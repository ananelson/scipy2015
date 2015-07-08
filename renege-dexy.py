# based on renege.py from https://bitbucket.org/simpy/simpy

import collections
import random
import simpy
import yaml
import json


### "moviegoer"
def moviegoer(env, movie, num_tickets, theater):
    with theater.counter.request() as my_turn:
        # Wait until its our turn or until the movie is sold out
        result = yield my_turn | theater.sold_out[movie]

        # Check if it's our turn of if movie is sold out
        if my_turn not in result:
            theater.num_renegers[movie] += 1
            env.exit()

        # Check if enough tickets left.
        if theater.available[movie] < num_tickets:
            # Moviegoer leaves after some discussion
            yield env.timeout(0.5)
            env.exit()

        # Buy tickets
        theater.available[movie] -= num_tickets
        if theater.available[movie] < 2:
            # Trigger the "sold out" event for the movie
            theater.sold_out[movie].succeed()
            theater.when_sold_out[movie] = env.now
            theater.available[movie] = 0
        yield env.timeout(1)

### "customer-arrivals"
def customer_arrivals(env, theater):
    while True:
        yield env.timeout(random.expovariate(1 / 0.5))

        movie = random.choice(theater.movies)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            env.process(moviegoer(env, movie, num_tickets, theater))

### "run"
Theater = collections.namedtuple('Theater', 'counter, movies, available, '
                                            'sold_out, when_sold_out, '
                                            'num_renegers')

def run(params_file):
    with open(params_file, 'r') as f:
        params = yaml.safe_load(f)
    random.seed(params['random-seed'])

    env = simpy.Environment()

    counter = simpy.Resource(env, capacity=1)
    movies = ['Python Unchained', 'Kill Process', 'Pulp Implementation']
    available = {movie: params['tickets'] for movie in movies}
    sold_out = {movie: env.event() for movie in movies}
    when_sold_out = {movie: None for movie in movies}
    num_renegers = {movie: 0 for movie in movies}
    theater = Theater(counter, movies, available, sold_out, when_sold_out,
                      num_renegers)

    # Start process and run
    env.process(customer_arrivals(env, theater))
    env.run(until=params['sim-time'])

    results = [{
        "name" : movie,
        "is-sold-out" : theater.sold_out[movie] and True or False,
        "sold-out-in" : theater.when_sold_out[movie],
        "queue-leavers" : theater.num_renegers[movie]
        } for movie in movies]

    with open("results.json", 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    run("settings.yaml")
