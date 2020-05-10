# -*- coding: utf-8 -*-

################################################################
import numpy as np
import pandas as pd
import random as random
import matplotlib.pyplot as plt
import random
import copy
from operator import attrgetter
from six.moves import range

#common methods
def get_portfolio_return(p_mean_daily_returns, p_weights,p_day_count):
    v_portfolio_return = np.sum(p_mean_daily_returns * p_weights) * p_day_count
    return v_portfolio_return

#calculate annualised portfolio volatility
def get_portfolio_std_dev (p_cov_matrix, p_weights, p_day_count):
    v_portfolio_std_dev = np.sqrt(np.dot(p_weights.T,np.dot(p_cov_matrix, p_weights))) * np.sqrt(p_day_count)
    return v_portfolio_std_dev

#### Inputs from earlier modules ###
#list of stocks in portfolio - by TradingName
def main_wrapper(stock_names, AmountCPFOA, risk_profile_string):

    #dictionary for risk profile
    Risk_Profile = {
        "Conservative": 4.6, "Moderately Conservative": 12.5, "Moderate": 20.9, "Moderately Agressive": 29.5, "Aggressive": 36.0
    }
    risk_from_schwab = None
    if risk_profile_string in Risk_Profile.keys():
        risk_from_schwab = Risk_Profile[risk_profile_string]

    print(risk_from_schwab, 'risk schwab')
    print('inside GA wrapper')
    print(risk_from_schwab, stock_names, AmountCPFOA, risk_profile_string, 'all payllooadadasda')

    print(stock_names, 'stock names')
    STOCK_NAMES = stock_names
    # Users Risk Profile - mapped to max Risk %
    MAX_RISK_ON_PORTFOLIO = risk_from_schwab
    # current Risk Free Returns from CPF-SA
    CPFSA_RETURNS = 0.04
    # CSV file with Stock Codes
    CSV_STOCK_CODES = "app/SGX Codes v4.csv"
    # CSV file with Stock Prices
    CSV_STOCK_PRICES = "app/SGX Prices v4.csv"
    #CPF OA - $20000 as that is the bare minimum you need inside for investments
    CPFOA = int(AmountCPFOA) - 20000

    #### System Options ===
    ##  Decide to include of exclude CPF
    INCLUDE_CPF = True

    ### start of code ####
    ######################
    num_stocks = len(STOCK_NAMES)
    stock_names = sorted(STOCK_NAMES)

    #sort the names & get stock symbols
    stock_mapping = pd.read_csv(CSV_STOCK_CODES)
    stock_symbols = stock_mapping[stock_mapping['Trading Name'].isin(stock_names)]['SGXCode'].tolist()

    #get the daily price data for each of the stocks in the portfolio
    #import pandas_datareader.data as web
    #data = web.DataReader(stock_symbols,data_source='yahoo',start='01/01/2019', end='01/01/2020')['Adj Close']
    data = pd.read_csv(CSV_STOCK_PRICES, index_col=0)[stock_symbols].sort_index()
    day_count = len(data.index)

    #convert daily stock prices into daily returns
    returns = data.pct_change()

    if INCLUDE_CPF:
        num_stocks = num_stocks + 1
        # Add CPF-SA to the names & returns
        stock_names = stock_names + ['CPF_SA']
        returns.insert(num_stocks-1, stock_names[num_stocks-1], [CPFSA_RETURNS / day_count]*day_count, True)

    #calculate mean daily return and covariance of daily returns
    mean_daily_returns = returns.mean()
    #ann_returns = mean_daily_returns * day_count

    #calculate covariance of daily returns
    cov_matrix = returns.cov()
    #pct_cov_matrix = cov_matrix * 10000
    print('after retrieving cov_matrix')
    #set array holding portfolio weights of each stock
    weights = np.asarray([1/num_stocks]*num_stocks)
    print('weights out')
   
    portfolio_return = get_portfolio_return(mean_daily_returns, weights,day_count)
    portfolio_std_dev = get_portfolio_std_dev(cov_matrix, weights, day_count)
    print('portfolio methods end')
    # print the results
    pModel = "Equi-Allocation Model"
    pReturn = portfolio_return
    pRisk = portfolio_std_dev
    pSharpe = pReturn/pRisk
    pAllocation = weights

    print (f"{pModel} (User Risk Appetite is {MAX_RISK_ON_PORTFOLIO})")
    print (f"Return :{round(pReturn*100,2)}%", end = "\t\t")
    print (f"Risk   :{round(pRisk*100,2)}%", end = "\t\t")
    print (f"Sharpe :{round(pSharpe,2)}")
    print ("\nStock Allocation:")
    for allocation in zip(stock_names, pAllocation):
        print (f"{allocation[0].ljust(len(max(stock_names, key=len)))} : {round(allocation[1]*100,2)}%")
    print("************************************************")

 ########################################################
    ##### Run Simulation & Plot Markwitz Bullet ##########
    #calculate annualised portfolio return
    #set number of runs of random portfolio weights
    num_portfolios = 25000

    #set up array to hold results
    #We have increased the size of the array to hold the weight values for each stock
    results = np.zeros((4 + num_stocks - 1,num_portfolios))
    print('cycling through portfolio')
    for i in range(num_portfolios):
        #select random weights for portfolio holdings total to 1
        weights = np.array(np.random.random(num_stocks))
        weights /= np.sum(weights)
    print('end of cyclic method')   
    # Alternate method as used in GA
    #weights = (np.random.dirichlet(np.ones(num_stocks),size=1)[0])

    #calculate portfolio return and volatility
    portfolio_return = get_portfolio_return(mean_daily_returns, weights,day_count)
    portfolio_std_dev = get_portfolio_std_dev(cov_matrix, weights, day_count)
    print('portfolio intermediary')
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = results[0,i] / results[1,i]
    print('portfolio intermediary1')
    #iterate through the weight vector and add data to results array
    for j in range(len(weights)):
            results[j+3,i] = weights[j]

    #convert results array to Pandas DataFrame
    t_columns = ['ret','stdev','sharpe'] + stock_names[:num_stocks]
    results_frame = pd.DataFrame(results.T,columns=t_columns)
    print('portfolio intermediary2')
    #locate position of portfolio with highest Sharpe Ratio
    max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]

    #locate positon of portfolio with minimum standard deviation
    min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

    #locate positon of portfolio with max returns within user variance
    in_risk_port = (results_frame.query(f"stdev <= {MAX_RISK_ON_PORTFOLIO}"))
    best_inrisk_port = results_frame.iloc[in_risk_port['ret'].idxmax()]

    # print the results
    pModel = "Randomized Model"
    pReturn = best_inrisk_port[0]
    pRisk = best_inrisk_port[1]
    pSharpe = pReturn/pRisk
    pAllocation = best_inrisk_port[3:]

    if not INCLUDE_CPF:
        print(f"Best Sharpe Portfolio \nReturns: {round(max_sharpe_port[0]*100,2)}% \t\tRisk : {round(max_sharpe_port[1]*100,2)}% \t\tSharpe : {round(max_sharpe_port[0]/max_sharpe_port[1],2)}")

        print (f"\n{pModel} (User Risk Appetite is {MAX_RISK_ON_PORTFOLIO})")
        print (f"Return :{round(pReturn*100,2)}%", end = "\t\t")
        print (f"Risk   :{round(pRisk*100,2)}%", end = "\t\t")
        print (f"Sharpe :{round(pSharpe,2)}")

        print ("\nStock Allocation:")
        for allocation in zip(stock_names, pAllocation):
            print (f"{allocation[0].ljust(len(max(stock_names, key=len)))} : {round(allocation[1]*100,2)}%")
        print("************************************************")

        #create scatter plot coloured by Min Vol, Inrisk, Best Sharpe Ratio,
        plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
        plt.xlabel('Volatility')
        plt.ylabel('Returns')
        plt.colorbar()
        #plot red star to highlight position of portfolio with highest Sharpe Ratio
        plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='b',s=1000)
        #plot green star to highlight position of minimum variance portfolio
        plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='r',s=1000)
        #plot blue star to highlight position of best returns within risk variance portfolio
        plt.scatter(best_inrisk_port[1],best_inrisk_port[0],marker=(5,1,0),color='g',s=1000)



#from pyeasyga.pyeasyga import GeneticAlgorithm

# Initialize with random seed
    seed = np.random.dirichlet(np.ones(num_stocks),size=1)[0]

    ga = CIA_GeneticAlgorithm(seed, population_size=50,
                                generations=500,
                                crossover_probability=0.8,
                                mutation_probability=0.1,
                                elitism=True,
                                maximise_fitness=True)
    ## Create individual chromosomes - Constraint : sum of weights = 1
    def create_individual(data):
        return (np.random.dirichlet(np.ones(num_stocks),size=1)[0]).tolist()

    ga.create_individual = create_individual

    ## Define CrossOver Method - Constraint : sum of weights = 1

    def crossover(parent_1, parent_2):

        index = random.randrange(1, len(parent_1))

        # crossover & rotate genes
        child_1 = parent_1[:index] + parent_2[index:]
        child_2 = parent_2[:index] + parent_1[index:]

        # normalize sum of weights to 1
        child_1 /= np.sum(child_1)
        child_2 /= np.sum(child_2)

        return child_1.tolist(), child_2.tolist()

    ga.crossover_function = crossover

    ## Create Mutation Method - Constraint : sum of weights = 1
    def mutate(individual):
        # replace individual with new randomized individual
        individual = create_individual(individual)

    ga.mutate_function = mutate


    ## Define Selection method  - Try Tournament Selection

    def tournament_selection(population):
        """Select a random number of individuals from the population and
        return the fittest member of them all.
        """
        if ga.tournament_size == 0: ga.tournament_size = 2
        members = random.sample(population, ga.tournament_size)
        members.sort(key=attrgetter('fitness'), reverse=ga.maximise_fitness)
        return members[0]

    ga.selection_function = tournament_selection

    ## Define Fitness function  Constraint: Std Dev must be within risk Profile

    def fitness (weights, data):
        fitness = 0

        portfolio_std_dev = get_portfolio_std_dev(cov_matrix, np.asarray(weights), day_count)
        risk = portfolio_std_dev

        if risk <= MAX_RISK_ON_PORTFOLIO:
            portfolio_return = get_portfolio_return(mean_daily_returns, np.asarray(weights),day_count)
            fitness = portfolio_return
            #print (f"Current Returns : {fitness} and Current Risk : {portfolio_std_dev}")

        return fitness

    ga.fitness_function = fitness

    # run the GA algo
    ga.run()

    # print the results
    pModel = "Optimized Model"
    pReturn = ga.best_individual()[0]
    pRisk = get_portfolio_std_dev(cov_matrix, np.asarray(ga.best_individual()[1]), day_count)
    pSharpe = pReturn/pRisk
    pAllocation = ga.best_individual()[1]

    print (f"\n{pModel} (User Risk Appetite is {MAX_RISK_ON_PORTFOLIO})")
    print (f"Return :{round(pReturn*100,2)}%", end = "\t\t")
    print (f"Risk   :{round(pRisk*100,2)}%", end = "\t\t")
    print (f"Sharpe :{round(pSharpe,2)}")
    print(CPFOA, 'CPFOA') 
    print ("\nStock Allocation:")
    for allocation in zip(stock_names, pAllocation):
        print (f"{allocation[0].ljust(len(max(stock_names, key=len)))} : ${round(allocation[1]*CPFOA,2)}")
    print("************************************************")
    print(pModel, 'data type for pmodel')
    stock_allocation = []
    for allocation in zip(stock_names, pAllocation):
        print('in allocation method')
        newlist = []
        newlist.append(f"{allocation[0].ljust(len(max(stock_names, key=len)))}")
        newlist.append(f"${round(allocation[1]*CPFOA,2)}")
        print(newlist)
        stock_allocation.append(newlist)
    print(stock_allocation, 'stockallo list')
    print(stock_allocation, 'transformed payload')
    Return = f"{round(pReturn*100,2)}%"
    Risk = f"{round(pRisk*100,2)}%"
    Rules_max_risk = f"{MAX_RISK_ON_PORTFOLIO}%"
    print('endga after optimised', )

    return Return, Risk, stock_allocation, CPFOA, Rules_max_risk 

  
########################################################
######## PY EASY GA - Adapted ###############################################

class CIA_GeneticAlgorithm(object):

    def __init__(self,
                 seed_data,
                 population_size=50,
                 generations=100,
                 crossover_probability=0.8,
                 mutation_probability=0.2,
                 elitism=True,
                 maximise_fitness=True):

        self.seed_data = seed_data
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness

        self.current_generation = []
        self.fitness_function = None
        self.tournament_size = 0

    def create_initial_population(self):
        """Create members of the first population randomly.
        """
        initial_population = []
        for _ in range(self.population_size):
            genes = self.create_individual(self.seed_data)
            individual = Chromosome(genes)
            initial_population.append(individual)
        self.current_generation = initial_population

    def calculate_population_fitness(self):
        """Calculate the fitness of every member of the given population using
        the supplied fitness_function.
        """
        for individual in self.current_generation:
            individual.fitness = self.fitness_function(
                individual.genes, self.seed_data)

    def rank_population(self):
        """Sort the population by fitness according to the order defined by
        maximise_fitness.
        """
        self.current_generation.sort(
            key=attrgetter('fitness'), reverse=self.maximise_fitness)

    def create_new_population(self):
        """Create a new population using the genetic operators (selection,
        crossover, and mutation) supplied.
        """
        new_population = []
        elite = copy.deepcopy(self.current_generation[0])
        selection = self.selection_function

        while len(new_population) < self.population_size:
            parent_1 = copy.deepcopy(selection(self.current_generation))
            parent_2 = copy.deepcopy(selection(self.current_generation))

            child_1, child_2 = parent_1, parent_2
            child_1.fitness, child_2.fitness = 0, 0

            can_crossover = random.random() < self.crossover_probability
            can_mutate = random.random() < self.mutation_probability

            if can_crossover:
                child_1.genes, child_2.genes = self.crossover_function(
                    parent_1.genes, parent_2.genes)

            if can_mutate:
                self.mutate_function(child_1.genes)
                self.mutate_function(child_2.genes)

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)

        if self.elitism:
            new_population[0] = elite

        self.current_generation = new_population

    def create_first_generation(self):
        """Create the first population, calculate the population's fitness and
        rank the population by fitness according to the order specified.
        """
        self.create_initial_population()
        self.calculate_population_fitness()
        self.rank_population()

    def create_next_generation(self):
        """Create subsequent populations, calculate the population fitness and
        rank the population by fitness in the order specified.
        """
        self.create_new_population()
        self.calculate_population_fitness()
        self.rank_population()

    def run(self):
        """Run (solve) the Genetic Algorithm."""
        self.create_first_generation()

        for _ in range(1, self.generations):
            self.create_next_generation()

    def best_individual(self):
        """Return the individual with the best fitness in the current
        generation.
        """
        best = self.current_generation[0]
        return (best.fitness, best.genes)

    def last_generation(self):
        """Return members of the last generation as a generator function."""
        return ((member.fitness, member.genes) for member
                in self.current_generation)


class Chromosome(object):
    """ Chromosome class that encapsulates an individual's fitness and solution
    representation.
    """
    def __init__(self, genes):
        """Initialise the Chromosome."""
        self.genes = genes
        self.fitness = 0

    def __repr__(self):
        """Return initialised Chromosome representation in human readable form.
        """
        return repr((self.fitness, self.genes))


########################################################