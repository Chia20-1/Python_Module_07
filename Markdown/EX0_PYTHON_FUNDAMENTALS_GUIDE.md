# Ex0 Python Fundamentals Guide

This guide is for the small fundamental roadblock that can appear while redoing
`ex0`. The abstract factory idea may be clear, but Python can still trip you up
with method definitions, constructors, return annotations, and object creation.

The goal here is to help you diagnose your own next step.

## 1. The Main Mental Model

In this exercise, you are mostly connecting three things:

```text
Factory method -> creates object -> object has methods like describe() and attack()
```

So whenever you feel stuck, ask:

```text
Am I defining a class?
Am I creating an object from a class?
Am I calling a method on an object?
```

Most Python mistakes in this exercise come from mixing up those three actions.

## 2. Class vs Object

A class is the blueprint.

An object is the actual thing created from the blueprint.

Example:

```python
class Flameling:
    pass
```

`Flameling` is the class.

```python
flameling = Flameling()
```

`flameling` is an object.

In your factory, you usually want to return an object, not the class itself.

Think:

```text
Factory should give me an actual creature I can use now.
```

That means the factory method normally returns something created with
parentheses:

```python
return SomeCreature()
```

## 3. Why Instance Methods Need `self`

When a method belongs to an object, Python passes the object itself as the first
argument.

That first argument is normally called `self`.

Example:

```python
class Creature:
    def describe(self):
        return self.name
```

When you call:

```python
creature.describe()
```

Python secretly treats it like:

```python
Creature.describe(creature)
```

That is why the method definition needs `self`.

If you write:

```python
def describe():
    ...
```

then Python has nowhere to put the object that called the method.

### Rule Of Thumb

If the method is called like this:

```python
object.method()
```

then define it like this:

```python
def method(self):
    ...
```

In your exercise, factory methods are called on factory objects:

```python
factory.create_base()
factory.create_evolved()
```

So the methods should be instance methods.

## 4. Constructor Arguments Must Match

The constructor is `__init__`.

It decides what information is required when creating an object.

Example:

```python
class Creature:
    def __init__(self, name, creature_type):
        self.name = name
        self.creature_type = creature_type
```

This means a creature needs two values when it is created:

```python
Creature("Flameling", "Fire")
```

If the constructor accepts only one value after `self`, then object creation must
pass only one value:

```python
class Creature:
    def __init__(self, creature_type):
        self.creature_type = creature_type
```

Then this matches:

```python
Creature("Fire")
```

### Debug Question

When you create a creature, ask:

```text
How many arguments does __init__ expect after self?
How many arguments am I passing inside the parentheses?
```

Those two numbers must match.

## 5. Strings vs Variable Names

This is a very common Python beginner trap.

These are not the same:

```python
Fire
"Fire"
```

`Fire` without quotes means:

```text
Look for a variable named Fire.
```

`"Fire"` with quotes means:

```text
Use the text value Fire.
```

If you have not created a variable named `Fire`, Python will complain.

For creature names, types, and attack text, you usually want strings.

Examples:

```python
"Flameling"
"Fire"
"Fire/Flying"
"Water"
```

### Debug Question

If you see a `NameError`, ask:

```text
Did I write text without quotes?
```

## 6. Type Annotation vs Function Call

This line has two different ideas in it:

```python
def create_base(self) -> Creature:
    ...
```

The part after `->` is a type annotation.

It says:

```text
This method should return a Creature.
```

It does not create a creature.

So this:

```python
-> Creature
```

is a hint.

But this:

```python
Creature()
```

is a function/class call.

It tries to create an object.

### Important Difference

Use the class name without parentheses in a return type annotation:

```python
def create_base(self) -> Creature:
    ...
```

Use parentheses when creating an object:

```python
return Flameling()
```

### Debug Question

Ask:

```text
Am I describing the type, or am I creating an object?
```

If describing the type, no parentheses.

If creating an object, use parentheses.

## 7. Return Type Should Match The Returned Value

If a method says:

```python
def attack(self) -> str:
```

then it should return a string:

```python
return "Flameling uses Ember!"
```

If a method says:

```python
def attack(self) -> None:
```

that means:

```text
This method returns nothing useful.
```

But in your battle/testing code, `attack()` is printed:

```python
print(creature.attack())
```

So `attack()` should give back text.

### Debug Question

Ask:

```text
Is someone printing or using the result of this method?
```

If yes, the method probably needs to `return` a value.

## 8. Parent And Child Classes

Your concrete creatures are child classes of `Creature`.

That means:

```text
Creature defines the shared behavior.
Concrete creatures fill in their specific details.
```

When a child class calls:

```python
super().__init__(...)
```

it is asking the parent class to initialize the shared data.

Example:

```python
class Creature:
    def __init__(self, creature_type):
        self.name = self.__class__.__name__
        self.creature_type = creature_type
```

Then a child might call:

```python
super().__init__("Fire")
```

That works because the parent expects one value after `self`.

### Debug Question

When using `super().__init__(...)`, ask:

```text
What does the parent __init__ require?
Am I passing exactly that?
```

## 9. The Factory's Job

A factory method should usually be boring.

It should mostly say:

```text
When someone asks for this product, return the correct object.
```

Example shape:

```python
class SomeFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return SomeBaseCreature()

    def create_evolved(self) -> Creature:
        return SomeEvolvedCreature()
```

The factory should not usually calculate attack text or describe the creature.

That belongs inside the creature.

## 10. How To Trace The Program In Your Head

Use this trace before running the file.

```text
1. main creates a factory object.
2. test_factory receives that factory object.
3. test_factory calls factory.create_base().
4. create_base returns a creature object.
5. test_factory calls base.describe().
6. test_factory calls base.attack().
```

Now check each step:

```text
Does the factory object have create_base(self)?
Does create_base return an actual creature object?
Does the creature object have describe(self)?
Does the creature object have attack(self)?
Does attack return a string?
```

This is a stronger debugging method than guessing.

## 11. Common Error Messages And What They Usually Mean

### `TypeError: ... takes 0 positional arguments but 1 was given`

Likely cause:

```text
You forgot self in an instance method.
```

Check methods like:

```python
def create_base(self):
def create_evolved(self):
def attack(self):
```

### `NameError: name 'Fire' is not defined`

Likely cause:

```text
You wrote text without quotes.
```

Use:

```python
"Fire"
```

not:

```python
Fire
```

### `TypeError: __init__() takes ... but ... were given`

Likely cause:

```text
The number of values passed during object creation does not match __init__.
```

Compare:

```python
def __init__(self, ...)
```

with:

```python
SomeClass(...)
```

### `TypeError: Can't instantiate abstract class ...`

Likely cause:

```text
A child class did not implement every abstract method required by the parent.
```

Check whether the method names and parameters match the abstract class.

## 12. A Simple Checklist For Ex0

Before running your solution, check these one by one:

1. Every instance method has `self`.
2. Text values like names and types use quotes.
3. Return annotations use class names, not class calls.
4. Object creation uses parentheses.
5. Constructor arguments match `__init__`.
6. `attack()` returns a string if the caller prints it.
7. Every concrete factory implements all abstract factory methods.
8. Every concrete creature implements all abstract creature methods.
9. Factory methods return creature objects, not random strings or unrelated data.
10. The caller does not need to know the exact creature class.

## 13. The Next-Step Formula

When you are stuck on a line, classify it:

```text
Am I defining a method?
Then I probably need self.
```

```text
Am I passing a word as data?
Then I probably need quotes.
```

```text
Am I writing a return type?
Then I use the class name without parentheses.
```

```text
Am I creating an object?
Then I use the concrete class name with parentheses.
```

```text
Am I calling the parent constructor?
Then my arguments must match the parent's __init__.
```

That is the practical roadmap. The pattern itself is not the hard part here;
the hard part is making each Python sentence mean exactly what you intend.
