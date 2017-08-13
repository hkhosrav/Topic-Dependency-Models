# Topic Generation Server

Start with `python server.py`. It will bind itself to `localhost:9000` and respond with JSON payloads to the root path.

## Request Format
`localhost:9000/
It accepts the following GET parameters:
* studentNumber <int>
* studentDiversity <int>
* questionDifficulty <int>
* competencyValue <int>
* modelClass <"dynamic" | "static">


## Response Format

```typescript
{
    "name": string,
    "data": {
        "nodes": string[],
        "edges":  [
            string, // Edge source
            string, // Edge target
            number, // Edge topic attempts
            number // Edge topic competency
        ][]
    }
}[]
```