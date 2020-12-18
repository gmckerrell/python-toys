# Puzzles
This folder contains some interview based puzzles, for which I've tried to provide some "production quality" solutions.

Each puzzle is split into a reusable, tested module (`PUZZLENAME.py`) and an example file  (`PUZZLENAME_example.py`) which provides the requested answers.

## PRODUCTION vs TEST code
In general your production code should try and minimise duplicate code (DRY principal https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and that is what I've strived to do in the body of these modules.

It is also always a good idea to try and automate the testing of any code that you write. As humans we are not very good at consistently repeating the same tasks identically and as a consequence any testing that is reliant on a flesh and blood human, is a point of risk for a project.

Unit-tests are intended to assert that the behaviour of the various functions/methods within a module/class are as designed. In fact there is a entire paradigm of development focused around writing those tests first (and expecting them to fail) and subsequently fleshing out the required behaviour to pass the test.
https://en.wikipedia.org/wiki/Test-driven_development

However when it comes to unit-tests it is *more* important that each individual test can be understood without the reader jumping back and forth through the code. It also means that each individual test can be changed (fixed) without impacting other tests.

Here's a stack overflow discussion which talks about this
https://stackoverflow.com/questions/6453235/what-does-damp-not-dry-mean-when-talking-about-unit-tests

## MONOLITHIC vs MODULAR code
It is more maintainable to split any solution up into appropriate chunks. Python modules can be used to segregate functional portions of your solution, meaning that once one area has been built and tested you don't even need to touch that file, when building other parts; reducing the risk of you breaking stuff :-)

In python the following line has special meaning

```python
if __name__ == "__main__":
  # do something here...
```

A python file can be use in one of two ways
1) directly executed by the python program
   e.g. `python PopularDrinks.py`
   
2) imported as a module into another python file.
    e.g. `import PopularDrinks`

If the first case is used then the special `__name__` variable will be set to `"__main__"` otherwise it will be the name of the module.
See the following for more details
https://www.freecodecamp.org/news/if-name-main-python-example/

_NB. If your python file doesn't use the "special" `__name__` line then when someone imports it any top level code will be executed (which may not be desirable)_

These puzzle solutions have been written to be used as modules, hence their unit-test code lives in the same file but will *only* be executed if you run the module directly. In normal use (using import) the unit-tests will not run.

## REQUESTS vs REQUIREMENTS
_*"I know what you said, but was that what you meant?"*_

Requirements gathering is one of the most challenging aspects of software development.

Very often a customer doesn't know what they actually need, and there is an iterative conversation that needs to keep going during the development cycle to ensure that the final product meets the "needs" of the customer.

These puzzles are very specific and narrow in their specification, and for a one-off implementation a quick-n-dirty solution may well suffice...

### BUT MEANWHILE IN THE REAL WORLD...

In the PopularDrinks puzzle the stated requirement is
- "Return the fewest number of drinks he must learn..."

As a software engineer it is important to sometimes think "outside the box".

What is the customer's requirement rather than his request?
- The lazy bartender will need to know
  - Which drinks must he learn
  - Which customers need which drinks

What edge cases will need to be accounted for?
- If multiple drinks are equally popular, which one should be chosen?
  - Does it matter?
  - Does it need to be repeatable?
  - Are there more constraints that should be accounted for?
    - cheapest?
    - quickest to make?
    - fewest ingredients?
    - biggest profit?

These are the sort of things you would talk to the customer about. He should be clarifying "WHAT" he wants but not "HOW" it should be done.

There is a balancing act here. Another software related acronym YAGNI ("You Aren't Gonna Need It" https://martinfowler.com/bliki/Yagni.html) suggests that you should steer clear of "feature creep" and only implement what is needed in the here and now.

However it always pays to think and understand the problem domain, and try and implement your minimal solution in such a way that it can be extended easily (make it maintainable and easy to understand)

**This is very hard to do well.** (I've still not cracked it 100% after 26 years in the industry :smile:)

