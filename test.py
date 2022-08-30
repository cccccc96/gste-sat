import aiger
from aiger.aig import *

filename = './example/rbFIFO-1-3-1_NoOutput.aag'
aig = aiger.load(filename)
sim = aig.simulator()  # Coroutine
next(sim)  # Initialize
print(sim.send(
    {
        'rst': 1,
        'clock': 0,
        'dataIn[0]': 0,
        'dataIn[1]': 0,
        'push': 1,
        'pop': 0
    }
))
print(sim.send(
    {
        'rst': 0,
        'clock': 0,
        'dataIn[0]': 0,
        'dataIn[1]': 1,
        'push': 1,
        'pop': 0
    }
))
print(sim.send(
    {
        'rst': 0,
        'clock': 0,
        'dataIn[0]': 1,
        'dataIn[1]': 0,
        'push': 1,
        'pop': 0
    }
))


print(sim.send(
    {
        'rst': 0,
        'clock': 0,
        'dataIn[0]': 1,
        'dataIn[1]': 1,
        'push': 0,
        'pop': 1
    }
))
print(sim.send(
    {
        'rst': 0,
        'clock': 0,
        'dataIn[0]': 1,
        'dataIn[1]': 1,
        'push': 0,
        'pop': 1
    }
))


# import aiger
# from aiger.aig import *
#
# filename = './example/rbFIFO-1-3-1_NoOutput.aag'
# aig = aiger.load(filename)
# sim = aig.simulator()  # Coroutine
# next(sim)  # Initialize
# print(sim.send(
#     {
#         'rst': 1,
#         'clock': 0,
#         'dataIn[0]': 0,
#         'dataIn[1]': 0,
#         'push': 1,
#         'pop': 0
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 0,
#         'dataIn[1]': 1,
#         'push': 1,
#         'pop': 0
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 0,
#         'push': 1,
#         'pop': 0
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 1,
#         'pop': 0
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 1,
#         'pop': 0
#     }
# ))
#
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 0,
#         'pop': 1
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 0,
#         'pop': 1
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 0,
#         'pop': 1
#     }
# ))
# print(sim.send(
#     {
#         'rst': 0,
#         'clock': 0,
#         'dataIn[0]': 1,
#         'dataIn[1]': 1,
#         'push': 0,
#         'pop': 1
#     }
# ))

