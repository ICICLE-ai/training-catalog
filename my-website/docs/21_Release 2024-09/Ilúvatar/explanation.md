---
tags:
  - CI4AI
---

# Explanation

## Why use Ilúvatar for research?

Ilúvatar provides the features and guarantees we find to be necessary to conduct high-quality, reproducible, and open research.

1. Load generation a first-class citizen of the system, making results easier to capture and analyze.
2. Fast, predictable, jitter-resistant function execution for reliable and repeatable experimentation.
3. An architecture designed to allow testing on a single worker node, or a cluster of load-balanced nodes.
4. The ability to run a load scenario on a live system or as a simulation, _using the same codebase_.
5. An extendible FaaS platform built for an open-source research community.

Details about the implementation can be found in the paper below.
How to use the various features and jump-starting your research can be found [in the Ilúvatar documentation](https://github.com/COS-IN/iluvatar-faas/blob/gpu-support/src/Il%C3%BAvatar/README.md).

A popular open-source platform used in research is OpenWhisk, but we have found it has high overheads under notable load, caused by a variety of factors.
The scalability of OpenWhisk vs our Ilúvatar can be seen here.

![Ilúvatar performance orchestrating functions](https://raw.githubusercontent.com/COS-IN/iluvatar-faas/gpu-support/imgs/overhead-scaling.jpeg)

We can ensure a constant 1-3 ms overhead on invocations at significant load, whereas OpenWhisk sees high and variable overheads, on the same hardware.
It also does not have the research-first features implemented in Ilúvatar.

See Ilúvatar in action for research [right here](https://github.com/COS-IN/iluvatar-faas/blob/gpu-support/src/Il%C3%BAvatar/docs/RESEARCH.md)

## More documentation / Questions

Ilúvatar supports a large variety of customization in configuration and setup, and methods of load generation and experimentation.
It is easy to create custom functions that run new Python programs, [information is in this document](https://github.com/COS-IN/iluvatar-faas/blob/gpu-support/src/Il%C3%BAvatar/docs/FUNCTIONS.md#preparing-code-to-be-functions).
Detailed documentation can be found [closer to the code](https://github.com/COS-IN/iluvatar-faas/blob/gpu-support/src/Il%C3%BAvatar/README.md).

If you have questions, want help working with Ilúvatar, or anything else, we have a [Discord server](https://discord.gg/r4CZ7bZhmJ).
Definitely gives faster answers than opening an issue for a question.

## Why 'Ilúvatar'?

The name 'Ilúvatar' comes from J.R.R. Tolkien's mythology, published in [*The Silmarillion*](https://tolkiengateway.net/wiki/The_Silmarillion), a history of the world prior to the events of his *Hobbit* and *Lord of the Rings* books.
[Ilúvatar](https://tolkiengateway.net/wiki/Il%C3%BAvatar) is the creator of the world, and orchestrated its form and development.
We don't see our platform as being the ultimate, final, or conclusive FaaS platform.
But as a FaaS platform, it controls and directs where and how Serverless functions are created and executed, across a possibly great variety of heterogeneity and network distance.
Thus the inspiration for its name.
