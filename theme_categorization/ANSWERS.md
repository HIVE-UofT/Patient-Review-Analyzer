# Answers to Your Questions

## 1. Are we giving reviews to LLM one by one?

**Yes, reviews are processed sequentially (one by one).**

Looking at `pipeline.py` lines 104-109:

```python
for review in iterator:
    result = self.process_review(review)
    results.append(result)

    if rate_limit and self.settings.rate_limit_delay > 0:
        time.sleep(self.settings.rate_limit_delay)
```

**Why sequential processing?**

- **Rate limit compliance**: Prevents overwhelming the API
- **Better error handling**: Each review can be retried independently
- **Progress tracking**: Easy to see which review is being processed
- **Resource management**: Avoids memory issues with large batches

**Could we batch them?**

- Technically yes, but HuggingFace Router doesn't support batch requests in the same way
- Sequential processing is more reliable and easier to debug
- The rate limiting delay (default 1 second) helps prevent rate limit errors

## 2. What Causes APIConnectionError?

See `CONNECTION_ERROR_GUIDE.md` for detailed causes. Common reasons:

### Network Issues

- Firewall blocking HTTPS connections
- Proxy/VPN interference
- Internet connectivity problems
- DNS resolution failures

### SSL/TLS Issues

- SSL handshake timeouts (what you're experiencing)
- Certificate validation failures
- TLS version mismatches

### Server Issues

- HuggingFace Router overloaded
- Server maintenance
- Geographic restrictions
- Rate limiting causing connection drops

### Configuration Issues

- Timeout too short (fixed: increased to 60s default)
- Incorrect base URL
- Invalid API token
- Missing network libraries

## 3. Enhanced Prompt

The prompt has been enhanced to:

- **Define key themes**: "Key themes are specific topics, concerns, or aspects of the healthcare experience that the patient mentions or talks about"
- **Provide clear instructions**: Step-by-step guidance
- **Emphasize context**: Match themes based on content and context
- **Require descriptions**: Explain why each theme applies

See `ENHANCED_PROMPT_LATEX.md` for the LaTeX version to use in your article.
