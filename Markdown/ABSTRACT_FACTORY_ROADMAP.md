# Abstract Factory Pattern Roadmap

This guide is written for your creature factory exercise. The goal is not just
to memorize the pattern, but to know what question to ask next while you build
it independently.

## 1. The Core Idea

An abstract factory is a class/interface whose job is:

> Create a related group of objects without the caller needing to know the
> exact concrete classes.

In your exercise, the related group is a creature family.

For example:

- A fire family can create a base fire creature and an evolved fire creature.
- A water family can create a base water creature and an evolved water creature.
- The battle code should not care whether the factory is fire, water, or
  another family later.

The important shift is this:

Instead of asking:

```text
Which exact creature class should I instantiate here?
```

you ask:

```text
Which factory family am I using, and what product do I need from it?
```

## 2. Factory Method vs Abstract Factory

These two patterns are easy to mix up.

### Factory Method

A factory method usually creates one kind of object.

Example idea:

```python
create_creature()
```

It answers:

```text
How do I create one product without hard-coding the concrete class?
```

### Abstract Factory

An abstract factory creates multiple related products.

Example idea:

```python
create_base()
create_evolved()
```

It answers:

```text
How do I create a whole compatible family of products?
```

In your exercise, the factory does not only create "a creature". It creates
related creature variants from the same family.

That is what makes it an abstract factory.

## 3. How Your Exercise Maps To The Pattern

Think of the pattern in four roles.

| Pattern Role | In Your Exercise | Responsibility |
| --- | --- | --- |
| Abstract Product | `Creature` | Defines what all creatures can do |
| Concrete Product | Fire/water creature classes | Implements actual creature behavior |
| Abstract Factory | `CreatureFactory` | Defines what every creature family must create |
| Concrete Factory | Fire/water factory classes | Creates one specific family of creatures |

The caller, such as battle/testing code, should depend on the abstract factory:

```text
Give me any CreatureFactory.
I will ask it for a base creature or evolved creature.
I do not need to know the concrete class names.
```

## 4. The Mental Model

Imagine a vending machine with themed buttons.

The caller does not open the machine and assemble the item manually. The caller
presses:

```text
base
evolved
```

The selected machine decides what comes out.

If the selected machine is a fire factory:

```text
base -> fire base creature
evolved -> fire evolved creature
```

If the selected machine is a water factory:

```text
base -> water base creature
evolved -> water evolved creature
```

The caller uses the same buttons for every family. That sameness is the power of
the pattern.

## 5. The Roadmap For Solving An Abstract Factory Exercise

Use this checklist whenever you feel stuck.

### Step 1: Identify The Product Family

Ask:

```text
What objects belong together?
```

In your case, the family is a group of creatures with the same theme or type.

Examples:

- Fire family
- Water family
- Electric family
- Nature family

Do not start by writing a factory. Start by knowing the family.

### Step 2: Identify The Product Types Inside Each Family

Ask:

```text
What different kinds of objects must every family provide?
```

In your case, every family must provide:

- A base creature
- An evolved creature

This is why your abstract factory needs methods like:

```python
create_base()
create_evolved()
```

If every family must create it, it belongs in the abstract factory.

### Step 3: Define The Abstract Product

Ask:

```text
What behavior should all created objects share?
```

In your case, all creatures should be usable as `Creature` objects.

That means the caller can do this without knowing the exact class:

```python
creature.describe()
creature.attack()
```

The abstract product gives the caller a stable interface.

### Step 4: Create Concrete Products

Ask:

```text
What are the actual objects for each family?
```

For a fire family:

```text
base creature
evolved creature
```

For a water family:

```text
base creature
evolved creature
```

Each concrete creature should focus only on creature behavior, such as its name,
type, and attack.

It should not decide which factory it belongs to.

### Step 5: Define The Abstract Factory

Ask:

```text
What must every factory be able to create?
```

The abstract factory should list the creation methods, but not create concrete
objects itself.

Conceptually:

```python
class CreatureFactory:
    def create_base(self):
        ...

    def create_evolved(self):
        ...
```

The key is that this class describes the contract.

It says:

```text
Any real creature factory must know how to create a base creature and an evolved
creature.
```

### Step 6: Create Concrete Factories

Ask:

```text
For this family, which concrete class should each method return?
```

A fire factory returns fire creatures.

A water factory returns water creatures.

The concrete factory is where concrete class names belong.

This is good:

```text
FireFactory knows about FireBaseCreature and FireEvolvedCreature.
```

This is less good:

```text
Battle code knows about FireBaseCreature and FireEvolvedCreature.
```

The factory hides those details from the rest of the program.

### Step 7: Use The Factory From Client Code

Ask:

```text
Can the caller work with the abstract factory instead of concrete classes?
```

The caller should receive a factory and use it like this:

```python
base = factory.create_base()
evolved = factory.create_evolved()
```

The caller should not need logic like:

```python
if type == "fire":
    creature = FireCreature()
elif type == "water":
    creature = WaterCreature()
```

That kind of branching is a sign the caller knows too much.

## 6. The Thinking Loop

When implementing, repeat this loop:

1. What family am I adding?
2. What products must that family provide?
3. Do those products share the expected interface?
4. Does my concrete factory return the right matching products?
5. Can the caller use the factory without knowing exact creature classes?

If the answer to number 5 is yes, you are probably using the pattern correctly.

## 7. How To Recognize You Need Abstract Factory

Abstract factory is useful when you see these signs:

- You have multiple families of related objects.
- Each family has the same product categories.
- You want client code to stay independent from concrete class names.
- You want to add a new family without rewriting the caller.

In your exercise, adding a new creature family should feel like this:

1. Create the new concrete creature classes.
2. Create a new concrete factory for that family.
3. Use the new factory wherever a `CreatureFactory` is expected.

The existing battle/testing logic should not need to know the new creature class
names.

## 8. A Practical Test For Yourself

After you implement a factory, ask:

```text
Could I pass this factory into the same function that already accepts another
factory?
```

For example, if a function can accept a fire factory and a water factory without
changing its code, then your abstraction is working.

If the function needs special cases like this:

```python
if factory_is_fire:
    ...
```

then the factory pattern is leaking.

## 9. Common Mistakes

### Mistake 1: Putting Too Much Logic In The Caller

Bad sign:

```text
The caller chooses exact creature classes.
```

Better:

```text
The caller chooses a factory, then asks the factory for creatures.
```

### Mistake 2: Making One Factory Create Unrelated Things

Bad sign:

```text
One factory creates fire base creature and water evolved creature.
```

Better:

```text
Each concrete factory creates one consistent family.
```

### Mistake 3: Forgetting The Abstract Product

Bad sign:

```text
Every creature has different method names.
```

Better:

```text
Every creature can be used through the same shared interface.
```

For example, the caller should be able to call `attack()` on any creature.

### Mistake 4: Treating The Abstract Factory As A Concrete Factory

Bad sign:

```text
CreatureFactory directly creates specific fire or water creatures.
```

Better:

```text
CreatureFactory only defines the methods.
FireFactory and WaterFactory create the actual objects.
```

## 10. Independent Exercise Strategy

If you need to complete or extend the exercise independently, use this order:

1. Read the caller code first.
2. Notice what methods it expects on the factory.
3. Read the abstract factory.
4. Make sure each concrete factory implements every required method.
5. Read the abstract product.
6. Make sure every concrete creature follows that product interface.
7. Add or fix one family at a time.
8. Run the program mentally before running it for real:

```text
main creates factory
factory creates base creature
factory creates evolved creature
caller calls describe and attack
```

This mental trace is one of the best ways to debug design pattern exercises.

## 11. Quick Self-Quiz

Use these questions to check your understanding.

1. What is the abstract factory responsible for?
2. What is a concrete factory responsible for?
3. Why should battle code depend on `CreatureFactory` instead of specific
   creature classes?
4. If you add an electric family, which new classes would you expect to add?
5. Should the abstract factory contain `if fire` or `if water` logic?

Suggested answers:

1. It defines the creation methods every family factory must provide.
2. It returns the concrete products for one specific family.
3. So the battle code can work with any family without changing.
4. Electric concrete creatures and an electric concrete factory.
5. No. Family-specific creation belongs in concrete factories.

## 12. The One-Sentence Memory Hook

Abstract factory means:

> "Give me a factory for this family, and I will ask it for compatible products
> without knowing their concrete classes."

For your exercise:

> "Give me a creature factory, and I will ask it for base and evolved creatures
> without knowing exactly which creature classes they are."
