Could be — but "poorly architected" covers a lot of ground, and the fix is very different depending on what's actually biting us. Before we commit to anything, I'd want to pin down where the pain is actually coming from.

A few questions:

- **What's the symptom?** "Slowing us down" can mean slow queries/runtime, slow to add features, lots of bugs, painful migrations, hard to onboard people, or fear of touching things. Which one(s)?
- **Where does it hurt most?** Is there a specific area (a particular service, table, ORM layer, the way we share models across teams) that keeps coming up, or is it diffuse?
- **Concrete recent examples?** A feature that took way longer than it should have, or a class of bug we keep hitting — those are usually more telling than the general feeling.

My honest take: the "rewrite the whole data layer" instinct is tempting but usually the wrong first move — big-bang rewrites tend to reproduce the same problems with newer code and cost a quarter we don't get back. More often the real issue is 2-3 specific things (no clear ownership of schema, leaky abstractions, missing indexes, an ORM fighting our access patterns) that we can fix incrementally and feel relief fast.

Want to grab 30 min to map out where the friction actually is? If you can drop a couple of concrete examples beforehand, I can come with a rough read on whether this is a targeted-fix situation or a genuine re-architecture one.