from abc import ABC, abstractmethod
from typing import List, Tuple
import nltk
import itertools
import random

class ParaphrasationAlgorithm(ABC):

    """
    Paraphrasation algorithm interface
    """

    @abstractmethod
    def paraphrase(self, t:nltk.Tree, limit=100) -> List[nltk.Tree]:
        pass



class DefaultParaphrasationAlgorithm(ParaphrasationAlgorithm):

    """
    Concrete realization of ParaphrasationAlgorithm according to test task
    """


    def __check_sub_tree(self, t:nltk.Tree) -> bool:
        """

        :param t: instance of nltk.Tree
        :return: True if subtree suitable for mutation False otherwise
        """

        if not isinstance(t, nltk.Tree): raise ValueError(f"wrong type of t, expected nltk.Tree got {type(t)} instead")

        labels = [el.label() for el in t]#get labels if all nodes in subtree
        NP_counts = labels.count("NP")#get number of NP nodes in subtree
        Coma_counts = labels.count(",")#get number of ',' nodes in subtree
        CC_counts = labels.count("CC")#get number of CC nodes in subtree

        return (NP_counts >= 2) and (Coma_counts + CC_counts >= 1) #subtree must include 2 or more NP nodes and at least one of ',' or CC nodes


    def __find_suitable_sub_trees(self, t:nltk.Tree) -> List[ Tuple[ Tuple[int], nltk.Tree]]:
        """
        :param t: instance of nltk.Tree
        :return: returns list of tuples of two elements, first element is a treepos of subtree suitable to mutate, second element is subtree itself
        """

        if not isinstance(t, nltk.Tree): raise ValueError(f"wrong type of t, expected nltk.Tree got {type(t)} instead")

        suitable_sub_trees = [] #subtrees suitable for mutation along with their treepos will be stored here

        for tree_pos in t.treepositions():
            curr_elem = t[tree_pos]
            if isinstance(curr_elem, nltk.Tree):
                if len(curr_elem) >= 3 and curr_elem.label() == "NP":
                    if self.__check_sub_tree(curr_elem):#checking if tree_node is a Tree itself and does it fit the condition
                        obj = (tree_pos, curr_elem)
                        suitable_sub_trees.append(obj)#if sub tree fits the condition store it and it's treepos

        return suitable_sub_trees

    def __mutate_sub_tree(self, t:nltk.Tree) -> List[nltk.Tree]:
        """
        :param t: instance of nltk.Tree
        :return: returns list of perephrased subtrees
        """

        if not isinstance(t, nltk.Tree): raise ValueError(f"wrong type of t, expected nltk.Tree got {type(t)} instead")

        treepos_to_mutate = []#treeposes of the nodes to permutate
        modified_trees = []#perephrased subtrees will be stored here
        for tree_pos in t.treepositions()[1:]:
            if isinstance(t[tree_pos], nltk.Tree) and t[tree_pos].label() == "NP": treepos_to_mutate.append(tree_pos)
        permutations = list(itertools.permutations(treepos_to_mutate))#get permutations of treepositions of NP nodes
        for perm in permutations:#perform permutations, just changing the order of NP nodes inside a subtree
            t_to_permute = t.copy(deep=True)
            for i in range(len(treepos_to_mutate)):
                cur_pos = treepos_to_mutate[i]
                elem_to_insert = t[perm[i]]
                t_to_permute[cur_pos] = elem_to_insert
            modified_trees.append(t_to_permute)
        return modified_trees


    def paraphrase(self, t:nltk.Tree, limit) -> List[nltk.Tree]:
        """
        :param limit: max number of generated trees
        :param t: instance of nltk.Tree
        :return: list of perephrased trees

        The idea behind this method is to find all NP subtrees that satisfy a condition of containing 2 or more NP nodes connected with ',' or CC
        then permutate each subtree by changing order of NP nodes inside the subtree and then find productions of all of modified subtrees
        """

        if not isinstance(t, nltk.Tree): raise ValueError(f"wrong type of t, expected nltk.Tree got {type(t)} instead")

        suitable_sub_trees = self.__find_suitable_sub_trees(t)
        modified_sub_trees = []
        for obj in suitable_sub_trees:
            pos, sub_tree = obj
            perephrased_sub_trees = self.__mutate_sub_tree(sub_tree)
            obj1 = (pos, perephrased_sub_trees)
            modified_sub_trees.append(obj1)

        productions = list(itertools.product(*[obj[1] for obj in modified_sub_trees]))

        modified_trees = []
        N = len(productions)
        if N - 1 > limit:
            indexes = random.sample(range(1, N), limit)
        else: indexes = range(1, N)
        for ind in indexes:
            prod = productions[ind]
            tree = t.copy(deep=True)
            for pos, sub_tree in enumerate(prod):
                treepos = modified_sub_trees[pos][0]
                tree[treepos] = sub_tree
            modified_trees.append(tree)

        return modified_trees



class Rephraser():

    """
    Class to implement Strategy Pattern
    """

    def __init__(self):
        self.__perephrasation_method:ParaphrasationAlgorithm = None
        self.__limit = 20

    def SetParaphrasationMethod(self, method:ParaphrasationAlgorithm) -> None:
        if not isinstance(method, ParaphrasationAlgorithm): raise ValueError(f"wrong type of method expected PerephrasationAlgorithm, got {type(method)} instead")
        else: self.__perephrasation_method = method

    def SetLimit(self, limit:int) -> None:
        if not isinstance(limit, int): raise ValueError(f"wrong type of limit, expected int got {type(limit)} instead")
        else: self.__limit = limit

    def ExecuteMethod(self, t:nltk.Tree) -> List[nltk.Tree]:
        if not isinstance(t, nltk.Tree): raise ValueError(f"wrong type of t, expected nltk.Tree got {type(t)} instead")
        else: return self.__perephrasation_method.paraphrase(t, limit=self.__limit)








