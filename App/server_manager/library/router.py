from srr import ShortestRouteResolver, NodeType
router = ShortestRouteResolver()

# -- Imports
import time


# -- Variables
UPDATE_INTERVAL = 5
tree_cache = None
tree_cache_time = time.time()



"""
    :name: get_latest_tree
    :return: str - The latest tree as a json string
    :description: Gets the latest tree from the resolver
        It stores the tree in a caching variable, and 
        only updates it every x seconds.
"""
def get_latest_tree(force: bool = False) -> str:
    global tree_cache, tree_cache_time

    # -- Check if the cache is valid
    if not force and tree_cache and time.time() - tree_cache_time < UPDATE_INTERVAL:
        return tree_cache
    
    # -- Update the cache
    tree_cache = router.to_json()
    tree_cache_time = time.time()
    return tree_cache


