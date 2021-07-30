CodeMirror.defineMode("asmarm", function ()
{
	var keywords1 = /^(lsl|(and|eor|sub|rsb|add|adc|sbc|rsc|orr|bic|swi|cmp|cmn|teq|tst|cdp|mrc|mcr)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|(mov|mvn)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?[s]?|(mul|mla)[l]?(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|(mul|mla)[l]?(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|(u|s)(mul|mla)[l](eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?[s]?|(mrs|msr)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|(ldr|str)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?[b]?[t]?|(ldr|str)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?(h|sb|sh)?|(ldm|stm)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?(fd|ed|fa|ea|ia|ib|da|db)?|(swp)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?[b]?|(ldc|stc)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?[l]?)\b/i;
	var keywords2 = /^(b(l|x)?(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|ret)\b/i;
	var keywords3 = /^(r[1]?[0-9]|lr|sp|pc)\b/i;
	var keywords4 = /^(align|CODE16)\b/i;
	var numbers = /^(0x[0-9a-f]+|0b[01]+|[0-9]+|[0-9][0-9a-f]+h|[0-1]+b)\b/i;
	return {
		startState: function () {
			return { context: 0 };
		},
		token: function (stream, state) {
			//if (!stream.column())
			//	state.context = 0;
			if (stream.eatSpace())
				return null;
			var w;
			if (stream.eatWhile(/\w/)) {
				w = stream.current();
				if (keywords1.test(w)) {
					//state.context = 1;
					return "keyword";
				} else if (keywords2.test(w)) {
					//state.context = 2;
					return "keyword-2";
				} else if (keywords3.test(w)) {
					//state.context = 3;
					return "keyword-3";
				} else if (keywords4.test(w)) {
					return "operator";
				} else if (numbers.test(w)) {
					return "number";
				} else {
					return null;
				}
			} else if (stream.eat(";")) {
				stream.skipToEnd();
				return "comment";
			} else if (stream.eat("!") || stream.eat(",") || stream.eat(".") || stream.eat(":") || stream.eat("[") || stream.eat("]") || stream.eat("+") || stream.eat("-") || stream.eat("*")) {
				return "operator";
			} else {
				stream.next();
			}
			return null;
		}
	};
});
CodeMirror.defineMIME("text/plain", "txt");

