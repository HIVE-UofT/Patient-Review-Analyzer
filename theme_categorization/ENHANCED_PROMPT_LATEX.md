# Enhanced Prompt - LaTeX Format for Article

## Complete LaTeX Code Block

Copy this directly into your LaTeX article:

```latex
\begin{tcolorbox}[colback=lightgray!10, colframe=black, fontupper=\ttfamily\footnotesize, sharp corners=southwest, rounded corners=northwest, enhanced jigsaw, boxrule=0.4pt]
prompt = (
"You are analyzing a patient review to identify key themes or areas discussed in the text. " \\
"Key themes are specific topics, concerns, or aspects of the healthcare experience that the patient " \\
"mentions or talks about in their review.\textbackslash n\textbackslash n" \\
"Analyze the following patient review and identify all key themes from this list: " \\
f"\{', '.join(KEY\_THEMES)\}.\textbackslash n\textbackslash n" \\
"Instructions:\textbackslash n" \\
"- Identify themes that represent topics, concerns, or areas explicitly mentioned or discussed in the review\textbackslash n" \\
"- A single review may contain multiple themes\textbackslash n" \\
"- Match themes based on the content and context of what the patient is describing\textbackslash n" \\
"- If no theme from the list matches the content, use 'unknown'\textbackslash n" \\
"- For each identified theme, provide a brief description explaining why this theme applies\textbackslash n\textbackslash n" \\
f"Patient Review:\textbackslash n\{patient\_review\}\textbackslash n\textbackslash n" \\
"Respond with a JSON object containing a list of identified themes in the format below:\textbackslash n" \\
"\{\textbackslash n" \\
"  \textbackslash"themes\textbackslash": [\textbackslash n" \\
"    \{\textbackslash n" \\
"      \textbackslash"theme\textbackslash": \textbackslash"\textbackslash",\textbackslash n" \\
"      \textbackslash"description\textbackslash": \textbackslash"\textbackslash"\textbackslash n" \\
"    \}\textbackslash n" \\
"  ]\textbackslash n" \\
"\}"
)
\end{tcolorbox}
```

## What Changed from Original Prompt

### Original Prompt:

- Simple instruction: "Analyze the following patient review and identify key themes"
- No definition of what "key themes" means
- Minimal guidance on how to match themes

### Enhanced Prompt:

- **Clear definition**: "Key themes are specific topics, concerns, or aspects of the healthcare experience that the patient mentions or talks about"
- **Detailed instructions**: Step-by-step guidance
- **Context emphasis**: "Match themes based on the content and context"
- **Description requirement**: "Provide a brief description explaining why this theme applies"

## Benefits

1. **Better understanding**: LLM knows exactly what "key themes" means
2. **More accurate matching**: Context-aware theme identification
3. **Consistent output**: Clear instructions lead to more consistent results
4. **Explainable results**: Descriptions help validate theme assignments
