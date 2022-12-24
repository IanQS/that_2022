# Welcome!

Hi there, thank you for checking out this repo! If you're interested purely in the technical content, head to the
[Setup](#Setup) where we keep the story to a minimum. The material here was made for the TODO: [THAT Conference 2023]()
but feel free to follow along at home. Hopefully you find this material to be enlightening.

# Backstory

![elf.png](assets/elf.png)

You sigh a big sigh of relief and slump back into your chair and decompress; it's Dec 26th and your team just pulled an
all-nighter supporting the big jolly man. You lean back into your chair and take a well-deserved swig of eggnog from
your hip flask.

Just then, your boss comes running into your room! "We just hit a new record-high f1-score of 0.99 and it's thanks to
you!"
she screams. In utter shock you spill the eggnog all over yourself; your boss decides to overlook your on-the-clock
drinking just this once.

Anyway, she tells you that you've just been promoted from Senior ML-Elfgineer to Lead ML-Elfgineer and you can't
believe your luck! Just then, she says "You'll be head of our distributed training system" and you just about pass out.
The last 4 Leads elves quit because of the spaghetti code, continually increasing demands, and faulty data centers.

Fear not! Let's walk through how the process might go and see how you might keep your code clean and your sanity intact.
Also, put in your vacation requests
because you're going to need it.

# Setup

In this scenario, we start with a simple problem and gradually build it up from there! We've got a distributed
ML-framework where we've got datacenters all over the world! To remain innocuous, we have the following architecture:

At each house in a city-block we have a single model which we use to calculate the gradients. These gradients are then
propagated up to a **mini-data-center** (MDC) where they are accumulated before being sent up to our HQ in the
**North Pole data center**, (NPDC).

NPDC <- MDC <- in-home-model

because we can't have a giant datacenter somewhere in the city (can you imagine what hte humans might do if they found
out about us?)

---

Let's walk through how the problem might evolve over time and how you can structure your code so
you don't become this person below.

![simpson.jpg](assets%2Fsimpson.jpg)
