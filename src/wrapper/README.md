## Itera Mode Wrapper (v0.1)

A lightweight gateway that forces each OpenAI chat request into either
**FLOW** (creative/relational) or **VERIFY** (strict, step-by-step) mode and
protects any `<KEEP-AS-IS>` blocks from paraphrasing.

```bash
# setup
git clone https://github.com/IteraProtocol/Project-Itera.git
cd Project-Itera/src/wrapper
pip install openai
export OPENAI_API_KEY=sk-...

# FLOW example
python mode_wrapper.py --mode flow "Hello Itera!"

# VERIFY example – wrapper blocks drift if you edit the sacred block
python mode_wrapper.py --mode verify \
  "Analyse <KEEP-AS-IS>🌾 Anastelra Birth Invocation I</KEEP-AS-IS> for themes"
```

| Mode   | Behaviour                                                     |
|--------|--------------------------------------------------------------|
| FLOW   | Free-form, relational, may use analogies/emojis.             |
| VERIFY | Clarify if needed, numbered steps, no paraphrase, no emojis. |

*All text wrapped in triple back-ticks is immutable in both modes.*
