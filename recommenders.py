from operator import itemgetter
import networkx as nx
import pandas as pd


def friends(graph, user):
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    x=[]
    
    for each in graph.neighbors(user):
        for item in graph.neighbors(each):
            x.append(item)
    
    return set(x)
   

def common_friends(graph, user1, user2):
    x1 = friends(graph, user1)
    x2 = friends(graph, user2)
    return set(x1&x2)
    

def number_of_common_friends_map(graph, user):
    new_dict = dict()
    
    for each in graph.nodes():
        if (each != user):
            if (each not in graph.neighbors(user)):
                new_dict[each] = len(common_friends(graph, each, user))
    
    return new_dict


def number_map_to_sorted_list(map):
    map = sorted(map.items(), key = itemgetter(1), reverse=True)
    return map


def recommend_new_users(user, n):
    rec = []
    df569 = pd.read_csv('people_info.csv')
    df569.sort_values(by=['followers_count'], inplace=True, ascending=False)
    most = df569['screen_name'].unique()
    most_followed = most.tolist()
    
    for i in range(n):
        rec.append(most_followed[i])
    
    return rec


def recommend_by_number_of_common_friends(graph, user, n):
    diction = dict()
    diction = number_of_common_friends_map(graph, user)
    diction = number_map_to_sorted_list(diction)
    recommendations = []
    
    for i in range(n):
        recommendations.append(diction[i])
    
    return recommendations


def show(user, m):
    with open("node_list.txt", "r") as file:
        userss= file.read().splitlines()

    train_graph = nx.read_weighted_edgelist('node_pair.txt', create_using=nx.DiGraph(), nodetype=str)
    
    if user not in userss:
        print("Recommendations for new user are")
        return(recommend_new_users(user, m))        
    else:
        print("Recommendations are")
        return(recommend_by_number_of_common_friends(train_graph, user, m))
