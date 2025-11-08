# Enhanced Prompt for Article

## Current Prompt (from article)

The current prompt in your article is:

```
prompt = (
"Analyze the following patient review and identify key themes from the list: " \\
f"\{', '.join(KEY\_THEMES)\}. If no theme is recognized, use 'unknown'. Multiple themes may be present.\textbackslash n\textbackslash n" \\
f"Review: '\{patient\_review\}'\textbackslash n\textbackslash n" \\
"Respond with a JSON object containing a list of identified themes in the format below\textbackslash n" \\
"themes: [\textbackslash n" \\
" \{\textbackslash n" \\
" \textbackslash"theme\textbackslash": \textbackslash"\textbackslash",\textbackslash n" \\
" \textbackslash"description\textbackslash": \textbackslash"\textbackslash"\textbackslash n" \\
" \},\textbackslash n" \\
"]"
)
```

## Enhanced Prompt (Recommended)

For better JSON parsing and consistency, use this enhanced version:

```
prompt = (
"Analyze the following patient review and identify key themes from the list: " \\
f"\{', '.join(KEY\_THEMES)\}. If no theme is recognized, use 'unknown'. Multiple themes may be present.\textbackslash n\textbackslash n" \\
f"Review: '\{patient\_review\}'\textbackslash n\textbackslash n" \\
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
```

## Key Improvements

1. **Proper JSON structure**: Wraps the response in `{}` braces to ensure valid JSON
2. **Clearer formatting**: Better indentation makes the expected format more obvious
3. **Consistent parsing**: Reduces parsing errors by explicitly showing the complete JSON structure

## LaTeX Format for Article

If you want to use the enhanced prompt in your LaTeX article, here's the formatted version:

```latex
\begin{tcolorbox}[colback=lightgray!10, colframe=black, fontupper=\ttfamily\footnotesize, sharp corners=southwest, rounded corners=northwest, enhanced jigsaw, boxrule=0.4pt]
prompt = (
"Analyze the following patient review and identify key themes from the list: " \\
f"\{', '.join(KEY\_THEMES)\}. If no theme is recognized, use 'unknown'. Multiple themes may be present.\textbackslash n\textbackslash n" \\
f"Review: '\{patient\_review\}'\textbackslash n\textbackslash n" \\
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
