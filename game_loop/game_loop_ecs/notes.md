



Components only have data, no logic.

All logic should be in the systems.


Entity has a unique id.

One global singleton registry for all entities, components, and systems, that can be load into the game.

Have archetypes too!



Monitoring system. Design first this. 
- a table with all the entities (rows) and their components (columns).


Game definition code organization:
-------
component definitions
- & archetypes
-------
system definitions
- & system groups
-------
entity definitions
- & flyweights
-------

run_game()



Engine code organization:

helper functions.
- add component
- add system
- add entity

base classes for components, systems, entities.


General design:
- central registry of everything
    - archetypes (systems query this)
- systems
    - query (by component names) -> each query is an archetype
    - job

References:
- https://awkravchuk.itch.io/cl-fast-ecs/devlog/622054/gamedev-in-lisp-part-1-ecs-and-metalinguistic-abstraction