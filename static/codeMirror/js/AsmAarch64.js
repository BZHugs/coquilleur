CodeMirror.defineMode("asmaarch64", function ()
{
	var keywords1 = /^((adc|add|neg|ngc|sub|and|bic)[s]?|(adr|adrp|cmn|cmp|madd|mneg|msub|mul|sdiv|smaddl|smngel|smsubl|smulh|smull|udiv|umaddl|umnegl|umsubl|umulh|umull)|(bfi|bfxil|cls|clz|extr|rbit|rev|rev16|rev32|sxtw)|(asr|eon|eor|lsl|lsr|mov|movk|movn|movz|mvn|orr|orn|ror|tst)|(ccmn|ccmp|cinc|cinv|cneg|csel|cset|csetm|csinc|csinv|csneg)|(ldp|ldpsw|prfm|stp)|(st|ld)[u]?[r]|(ld)[u]?[rs](b|h)?|(ld)[u]?[rsw]|(st|ld)[u]?[r](b|h)?|(at|brk|clrex|dmb|dsb|eret|hvc|isb|mrs|msr|nop|srv|sev|sevl|smc|svc|wfe|wfi|yield)|(dc|ic|tlbi)|()(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|(cbnz|cbz|tbnz|tbz|b|bl|blr|br|ret))\b/i;
	var keywords2 = /^(|(b)(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?)\b/i;
	var keywords3 = /^((x|w)[1-3]?[0-9]|lr|sp|pc|xzr)\b/i;
	var keywords4 = /^(ptr)\b/i;
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
			} else if (stream.eat(",") || stream.eat(".") || stream.eat(":") || stream.eat("[") || stream.eat("]") || stream.eat("+") || stream.eat("-") || stream.eat("*")) {
				return "operator";
			} else {
				stream.next();
			}
			return null;
		}
	};
});
CodeMirror.defineMIME("text/plain", "txt");
