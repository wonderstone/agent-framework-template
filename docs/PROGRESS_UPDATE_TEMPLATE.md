# Progress Update Template

This document defines a stable in-progress update shape for long-running or while-style tasks.

It is the companion to `docs/CLOSEOUT_SUMMARY_TEMPLATE.md`:

- this template is for progress checkpoints
- the closeout template is for terminal completion

## Recommended Template

```md
• 当前在做: [current action or batch summary] | 下一步: [next concrete action]
```

## Why This Shape

`•` is visually lightweight and avoids being mistaken for the final closeout footer.

The wording avoids terminal phrases such as:

- finished
- complete
- wrapped up
- final

unless the update is actually the true closeout boundary.

## Checkpoint Variant

```md
• 当前聚焦: [focus when needed] | 当前批次: [progress unit] | 下一步: [next progress unit]
```

## Rules For Good Use

Do:

- say what progress unit just finished
- say explicitly that work is continuing when it is
- keep the `Next` field concrete
- keep the line short enough that repeated updates do not feel like repeated closeout wrappers

Do not:

- use the final closeout marker `📍`
- imply the whole task is done when only one batch ended
- emit host closeout actions from a progress update

## Default Recommendation

For adopters of this template, the preferred default is:

```md
• 当前在做: [current progress unit summary] | 下一步: [next progress unit or blocker]
```
