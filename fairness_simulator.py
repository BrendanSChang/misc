# import matplotlib.pyplot as plt


class Tenant:
    def __init__(self, name):
        self.name = name
        self.last_allocated = 0
        self.total_allocated = 0

    def allocated(self, time):
        self.last_allocated = time
        self.total_allocated += 1


class Demand:
    def __init__(self, name, src, dst, tenant, cost):
        self.name = name
        self.src = src
        self.dst = dst
        self.tenant = tenant
        self.cost = cost
        self.tokens = 0
        self.last_allocated = 0
        self.total_allocated = 0
        self.metric = 0.

    def allocated(self, time):
        self.last_allocated = time
        if self.tokens == self.cost:
            self.total_allocated += 1
            self.tenant.allocated(time)
            self.tokens = 0
            return True

        # self.last_allocated -= .1
        self.tokens += 1
        return False

    def update(self, time):
        self.metric = time - self.last_allocated

    def adjust_metric(self):
        self.metric /= 2.


class Component:
    def __init__(self, name):
        self.name = name
        self.tenants = {}
        self.demands = []
        self.history = []

    def update(self, time):
        for d in self.demands:
            d.update(time)

    def match(self, time):
        matched = []
        choice = []
        srcs = set()
        dsts = set()
        ordered = sorted(self.demands, key=lambda x: x.metric, reverse=True)
        for d in ordered:
            if d.src not in srcs and d.dst not in dsts:
                if d.allocated(time):
                    matched.append(d)
                    choice.append("{0}-{1}".format(d.src, d.dst))
                    srcs.add(d.src)
                    dsts.add(d.dst)

        self.history.append(choice)

        self.update(time)

        high = 0
        low = 99999    # arbitrary, should fix later.
        for ten_name in self.tenants:
            t = self.tenants[ten_name]
            if t.total_allocated > high:
                high = t.total_allocated
            if t.total_allocated < low:
                low = t.total_allocated
        fair = (high - low) < 3    # arbitrary, should fix later

        fair = True
        return (matched, fair)

    def show_demands(self, prefix):
        for d in self.demands:
            print "{0}{1}-{2}:".format(prefix, d.src, d.dst)
            print (
                "{0}\tmetric={1}, last={2}, total={3}"
                    .format(
                        prefix,
                        d.metric,
                        d.last_allocated,
                        d.total_allocated
                    )
            )

    def show_tenants(self, prefix):
        high = 0
        low = 99999 # arbitrary, should fix later.
        for ten_name in self.tenants:
            t = self.tenants[ten_name]
            if t.total_allocated > high:
                high = t.total_allocated
            if t.total_allocated < low:
                low = t.total_allocated

            print (
                "{0}{1}: last={2}. total={3}"
                    .format(
                        prefix,
                        t.name,
                        t.last_allocated,
                        t.total_allocated
                    )
            )

        print ("{0}high: {1}, low: {2}, diff: {3}"
                    .format(prefix, high, low, high-low))

    def show(self, prefix):
        self.show_demands(prefix)
        self.show_tenants(prefix)

    def print_history(self):
        print self.history


NUM_COMPONENTS = 1
DEMAND_DIST = [
    [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]
]
TENANT_DIST = [
    [
        ['B', '-', '-'],
        ['A', '-', '-'],
        ['A', 'A', 'B']
    ]
]
COST_DIST = [
    [
        [0, 0, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
]
NUM_ITERATIONS = 50


if __name__ == '__main__':
    components = []
    choices = []
    demandMap = {}

    for i in xrange(NUM_COMPONENTS):
        comp = Component(i)
        demands = DEMAND_DIST[i]
        tenants = TENANT_DIST[i]
        costs = COST_DIST[i]
        count = 0
        for j in xrange(len(demands)):
            for k in xrange(len(demands[j])):
                if demands[j][k]:
                    ten_name = tenants[j][k]
                    if ten_name not in comp.tenants:
                        comp.tenants[ten_name] = Tenant(ten_name)
                    comp.demands.append(Demand(count, j, k, comp.tenants[ten_name], costs[j][k]))
                    count += 1

        components.append(comp)
        choices.append([])

    counter = 0
    for c in components:
        for d in c.demands:
            demandMap[d] = counter
            counter += 1
    y = range(counter)

    counter = 1
    valid = True
    while valid and counter <= NUM_ITERATIONS:
        print "Iteration {0}".format(counter)
        senders = []
        alloced_tenants = set()
        for i in xrange(len(components)):
            c = components[i]
            alloced, valid = c.match(counter)

            s = "Alloced: "
            for d in alloced:
                senders.append(demandMap[d])
                alloced_tenants.add(d.tenant)
                s += "{0}-{1}, ".format(d.src, d.dst)
            print "\t{0}".format(s[:-2])

        choices.append(senders)

        for c in components:
            for d in c.demands:
                if d.tenant in alloced_tenants:
                    d.adjust_metric()

        for c in components:
            print "\tComponent {0}:".format(c.name)
            c.show("\t\t")

        counter += 1

    print "Total allocations across tenants are fair: {0}\n".format(valid)
    for c in components:
        print "Component {0} history:".format(c.name)
        c.print_history()

    '''
    yticks = []
    for i in xrange(len(components)):
        c = components[i]
        for d in c:
            yticks.append("{0}:{1}-{2}".format(i, d.tenant.name, d.name))
    plt.yticks(y, yticks)

    x = range(1, counter)
    for c in choices:
        plt.plot(x, c)
    plt.show()
    '''
