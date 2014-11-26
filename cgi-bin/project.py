import os, operator, sys, re, subprocess, mimetypes, json
from settings import PROJECT_PATH, PROJECT_URL, MAKE
from urlparse import urljoin
from pprint import pprint
from itertools import tee, izip


MIME_TYPES = {}
MIME_TYPES['md'] = "text/markdown"
MIME_TYPES['markdown'] = "text/markdown"
MIME_TYPES_BYBASE = {}
MIME_TYPES_BYBASE['makefile'] = "text/makefile"

def guessmime (f):
    if os.path.isdir(f):
        return "inode/directory"
    _, ext = os.path.splitext(f)
    base = os.path.basename(f)
    ret = MIME_TYPES_BYBASE.get(base)
    if ret == None:
        ext = ext.lstrip(".").lower()
        ret = MIME_TYPES.get(ext)
        if ret == None:
            ret = mimetypes.guess_type(f)[0]
    return ret or ""

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

# def grouper(iterable, n, fillvalue=None):
#     "Collect data into fixed-length chunks or blocks"
#     # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
#     args = [iter(iterable)] * n
#     return izip_longest(fillvalue=fillvalue, *args)

textchars = bytearray([7,8,9,10,12,13,27]) + bytearray(range(0x20, 0x100))
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

def is_binary_file (path):
    with open(path, 'rb') as f:
        return is_binary_string(f.read(1024))

def is_filename (f):
    base, ext = os.path.splitext(f)
    return len(ext) > 1

class Project (object):
    def __init__(self, path, create=False):
        self.fullpath = os.path.abspath(os.path.join(PROJECT_PATH, path))
        if os.path.exists(self.fullpath) and not os.path.isdir(self.fullpath):
            raise OSError("Project must be a directory ({0})".format(self.fullpath))
        absproj = os.path.abspath(PROJECT_PATH)
        (parent, _) = os.path.split(self.fullpath)
        if parent != absproj:
            raise OSError("Bad project path")
        self.path = os.path.relpath(self.fullpath, absproj)
        self.url = urljoin(PROJECT_URL, self.path) + "/"

        if not os.path.exists(self.fullpath) and create:
            os.mkdir(self.fullpath)

    def items (self):
        itemsByPath = {}
        for base, dirs, files in os.walk(self.fullpath):
            for p in files:
                fp = os.path.join(base, p)
                relpath = os.path.relpath(fp, self.fullpath)
                item = ProjectItem(self, relpath)
                itemsByPath[relpath] = item

        remake, missing = self.check_makefile()
        for i in missing:
            item = ProjectItem(self, i, exists=False)
            itemsByPath[i] = item
        for i in remake:
            item = itemsByPath[i]
            item.remake = True
        return [itemsByPath[x] for x in sorted(itemsByPath.keys())]

    def check_makefile (self):
        """
        Runs make -n --debug=v on project folder and searches for patterns:
        File `...' does not exist  ==> missing
        Must remake target `...'   ==> remake
        """
        try:
            output = subprocess.check_output([MAKE, "-n", "--debug=v"], cwd=self.fullpath)
            missingpat = re.compile(r"^\s*File\ \`(.+?)\'\ does\ not\ exist\.\s*$", re.M)
            remakepat = re.compile(r"^\s*Must\ remake\ target\ \`(.+?)\'\.\s*$", re.M)
            missing = [x for x in missingpat.findall(output) if is_filename(x)]
            remake = [x for x in remakepat.findall(output) if is_filename(x)]
            return remake, missing        
        except subprocess.CalledProcessError, e:
            return [], []

    def _dict (self):
        ret = {}
        ret['path'] = self.path
        ret['url'] = self.url
        ret['items'] = [x._dict() for x in self.items()]
        return ret  

    def json (self):
        items = self.items()
        return json.dumps(items)



class ProjectItem (object):
    def __init__(self, project, path, exists=True, remake=False):
        self.project = project
        self.path = path
        self.basename = os.path.basename(path)
        self.base, self.ext = os.path.splitext(self.basename)
        self.ext = self.ext.lstrip(".").lower()
        self.exists = exists
        self.remake = remake
        self.fullpath = os.path.join(project.fullpath, self.path)
        self.url = urljoin(project.url, path)
        self.mime_type = None
        self.size = None
        self.binary = False
        self.directory = False
        if exists:
            self.directory = os.path.isdir(self.fullpath)
            self.mime_type = guessmime(self.fullpath)
            self.size = os.path.getsize(self.fullpath)
            self.binary = is_binary_file(self.fullpath)

    def status (self):
        """
        .: exists and up to date,
        m: exists but needs to be remade,
        M: file doesn't yet exist, but can be made
        """
        status = "."
        if self.remake:
            if self.exists:
                status = "m"
            else:
                status = "M"
        return status        

    def __repr__ (self):
        return """<ProjectItem {1} {0}>""".format(self.path, self.status())

    def _dict (self):
        d = {}
        d['path'] = self.path
        d['exists'] = self.exists
        d['directory'] = self.directory
        d['remake'] = self.remake
        d['url'] = self.url
        d['basename'] = self.basename
        d['base'] = self.base
        d['ext'] = self.ext
        d['mime_type'] = self.mime_type
        d['size'] = self.size
        d['binary'] = self.binary
        return d

    def json (self):
        return json.dumps(self._dict())



if __name__ == "__main__":
    p = Project(sys.argv[1])
    # pprint (p._dict())

    items = p.items()
    for item in items:
        print item.status(), item.path
    #     print item.json()


