




# -------------------- 1.1. DESIGN SPAWN AND PATHFINDING -----------------------
'''
entities:
    - orc spawner (position, spawn-plan)
    - orc (position, velocity, path)
    - path (position, path)
    - map:
        - path
        - unwalkable
    - paths

components:
    - position (x, y, z)
    - renderable (sprite/model)
    - velocity (x, y, z)
    - spawn-plan (list of orc types and amounts and their arrival times)
    - path (list of positions)
    
    
systems:
    - monitoring system
    - spawn system
        - span plan, a list of orc types and amounts and their arrival times, and their path on the map
    - movement system
        - move orc based on velocity
        - follow path
    - rendering group
        - render map
        - render paths
        - render orcs
'''


# -------------------- 1.2. DESIGN FIRE AND BULLET -----------------------



# -------------------- 1.3. DESIGN EXPLOSION -----------------------







# -------------------- 1.4. DESIGN ECONOMY -----------------------





# -------------------- DESIGN MINIMAL IMPLEMENTATION -----------------------
'''
entities:
- 3 orcs
- 3 towers
- 1 orc spawner
- 1 home gate
- many paths
- many tower placement grids

components:
    - position (x, y, z)
    - renderable (sprite/model)
    - velocity (x, y, z)
    - health (hp)
    - weapon (cooldown, projectile-type, target-range, activation-range)
    - bullet (position, target-position, velocity)
    - explosion (position, area radius, damage)
    - spawn-plan (list of orc types and amounts and their arrival times)
    - home gate (position, health)
    - map-grid (position, renderable):
        - path
        - unwalkable
        - tower placement
        - orc spawner
        - home gate


systems:
    - spawn system
        - span plan, a list of orc types and amounts and their arrival times, and their path on the map
    - movement system
    - fire system (weapon, bullet, explosion)
    - spawn system (spawn-plan)
    - ai system)
'''








# -------------------- DESIGN INTERMEDIATE IMPLEMENTATION -----------------------





# -------------------- DESIGN OF FINAL IMPLEMENTATION -----------------------

# components and archetypes
'''
archetypes:
    - units (position, renderable): 
        - tower (level, projectile-type): 
            - medium-range
            - sniper
            - canon
            - near-field
            - freezer
        - orc (velocity)
            - small
            - medium
            - large
    - projectile (position, target-position, velocity): 
        - shell (+ explosion-type): 
        - bullet (+ damage)
    - explosion (position, area radius): 
        - cannon explosion (+ damage)
        - ice explosion (+ damage, slowdown-factor)
    - orc death:
        - orc
    - orc spawner (position, spawn-plan)
    - home gate (position, health)
    - map-grid (position, renderable):
        - path
        - unwalkable
        - tower placement
        - orc spawner
        - home gate
    - resources:
        - gold
    - ui_elements:
        - health bar
        - tower selection menu
        - wave indicator
        - score display
        - upgrade options        

components:
    - position:
        - x
        - y
        - z
    - target-position:
        - x
        - y
        - z
    - velocity:
        - x
        - y
        - z
    - health (hp):
        - current_health
        - max_health
    - weapon:
        - cooldown
        - projectile-type
        - range
    - damage:
        - amount (hp)
        - radius (for area effects)
    - slowdown-factor:
        - percentage
        - duration
        - radius (for area effects)
    - status_effects:
        - slowed
        - poisoned
        - burning
        - frozen
        - buffed/debuffed
    - spawn-plan:
        - list of orc types and amounts and their arrival times
    - economy:
        - cost
        - value (when destroyed)
        - income_generation
    - upgrade:
        - level
        - upgrade_paths
        - requirements
    - ai:
        - behavior_type
        - aggression_level
        - special_abilities
    - visual:
        - sprite/model
        - animation_state
        - visual_effects
    - audio:
        - sound_effects
        - trigger_conditions
        
    
'''
# systems and system groups
'''
Systems:
    - MovementSystem:
        - Updates positions based on velocities
        - Handles path following for enemies
        - Manages projectile trajectories
    
    - CombatSystem:
        - DetectionSystem: Identifies targets within range
        - AttackSystem: Initiates attacks when conditions are met
        - DamageSystem: Applies damage to health components
        - ProjectileSystem: Creates and manages projectiles
    
    - StatusEffectSystem:
        - Applies status effects (slow, poison, etc.)
        - Manages duration and intensity of effects
        - Removes expired effects
    
    - EconomySystem:
        - ResourceManagement: Tracks player resources
        - RewardSystem: Grants resources for defeating enemies
        - CostSystem: Handles tower building/upgrading costs
    
    - WaveSystem:
        - EnemySpawning: Controls timing and types of enemies
        - DifficultyScaling: Adjusts enemy stats based on wave
        - WaveProgression: Manages wave transitions
    
    - UISystem:
        - HealthBarRenderer: Shows current health status
        - ResourceDisplay: Shows player resources
        - TowerSelectionInterface: Manages tower placement UI
        - WaveIndicator: Shows current/upcoming waves
    
    - CollisionSystem:
        - Detects collisions between entities
        - Handles projectile impacts
        - Manages area effect applications
    
    - UpgradeSystem:
        - Manages tower upgrade paths
        - Applies stat improvements
        - Unlocks special abilities
    
    - AISystem:
        - PathfindingSystem: Determines optimal paths for enemies
        - BehaviorSystem: Controls enemy decision making
        - TargetingSystem: Selects optimal targets for towers
    
    - LifecycleSystem:
        - EntityCreation: Spawns new entities
        - EntityDestruction: Removes defeated/expired entities
        - TransformationSystem: Handles entity state changes

System Groups (execution order):
    1. InputSystemGroup:
        - PlayerInputSystem
        - UIInteractionSystem
    
    2. SimulationSystemGroup:
        - WaveSystem
        - AISystem
        - CombatSystem
        - MovementSystem
        - CollisionSystem
        - StatusEffectSystem
        - LifecycleSystem
        - EconomySystem
        - UpgradeSystem
    
    3. PresentationSystemGroup:
        - UISystem
        - RenderSystem
        - AudioSystem
        - ParticleSystem
        - AnimationSystem
'''

# entities and flyweights


# game loop
