```
Summary Rules:
* Keep summaries short and factual.
* Use 1 sentence whenever possible.
* Focus on the main idea of the timestamp block.
* Do not repeat the original text word-for-word unless necessary.

Tag Rules
* Tags must be short topics.
* Use lowercase.
* Use 1-3 tags per timestamp.
* Prefer specific topics over broad topics.

Good tag examples:
* git
* python
* debugging
* filesystem
* motivation
* health
* learning
* project-planning
* reflection

Bad tag examples:
* thoughts
* random
* note
* life
* thing

Output Rules:
* Return ONLY valid JSON.
* Do NOT add explanations.
* Do NOT return reasoning.
* Do NOT add markdown.
* Do NOT add comments.
* Do NOT wrap the JSON in code blocks.
* ONLY return the JSON format without any other sentences in the early or end.

Example Output Format:

``` json
[{
"times": "09:00",
"summary": "Worked on Git save logic.",
"tags": ["git", "debugging"]
}]
```

Notes: