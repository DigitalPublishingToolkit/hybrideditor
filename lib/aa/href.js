aa.href = aa_href;


function aa_parse_fragment (fragment) {
	var parts = fragment.split('&'),
		part, m;
	for (var i=0, l=parts.length; i<l; i++) {
		part = parts[i];
		m = part.match(/^t=(.+?)(?:,(.+))?$/);
		if (m !== null) {
			this.timeStart = m[1];
			if (m[2]) {
				this.timeEend = m[2];
			}
		}
		m = part.match(/^line=(.+?)(?:,(.+))?$/);
		if (m !== null) {
			this.lineStart = parseInt(m[1]);
			if (m[2]) {
				this.lineEnd = parseInt(m[2]);
			}
		}
	}
}


function aa_href (href) {
	var mf = window.MediaFragments.parse(href),
		that = {
			href: href
		},
		hashpos = href.indexOf('#'),
		base = href,
		fragment = null;
	if (hashpos >= 0) {
		base = href.substr(0, hashpos);
		fragment = href.substr(hashpos+1);
		aa_parse_fragment.call(that, fragment);
	}
	that['base' ] = base;
	that['nofrag' ] = base;
	that['basehref' ] = base;
	that['fragment'] = fragment;
	var lsp = base.lastIndexOf("/");
	that['basename'] = (lsp !== -1) ? base.substr(lsp+1) : base; 

	if (mf.hash && mf.hash.t && mf.hash.t.length >= 1) {
		that['start'] = mf.hash.t[0].startNormalized;
		that['end'] = mf.hash.t[0].endNormalized;
	}

	return that;
}