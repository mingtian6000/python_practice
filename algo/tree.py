class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
def postorder_traversal(root):
    def helper(node):
        if node:
            helper(node.left)
            helper(node.right)
            print(node.val, end=" ")
    helper(root)
    
#build this tree
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

postorder_traversal(root)