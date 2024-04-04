package com.template;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public class TreeNode {
    public int val;
    public TreeNode left;
    public TreeNode right;
    public TreeNode(int x) { val = x; }

    // 将输入字符串解析并构建二叉树
    public static TreeNode parseTreeNode(String inputStr) {
        // 使用Gson解析字符串为Integer列表
        Gson gson = new Gson();
        Type listType = new TypeToken<List<Integer>>(){}.getType();
        List<Integer> dataList = gson.fromJson(inputStr, listType);
        
        // 构建并返回二叉树
        return constructTreeNodeFromList(dataList);
    }
    
    // 辅助方法：根据列表构建二叉树
    public static TreeNode constructTreeNodeFromList(List<Integer> data) {
        if (data == null || data.isEmpty()) {
            return null;
        }
        TreeNode root = new TreeNode(data.get(0));
        LinkedList<TreeNode> nodeQueue = new LinkedList<>();
        nodeQueue.add(root);

        int i = 1;
        while (i < data.size()) {
            TreeNode currentNode = nodeQueue.poll();

            if (i < data.size() && data.get(i) != null) {
                currentNode.left = new TreeNode(data.get(i));
                nodeQueue.add(currentNode.left);
            }
            i++;

            if (i < data.size() && data.get(i) != null) {
                currentNode.right = new TreeNode(data.get(i));
                nodeQueue.add(currentNode.right);
            }
            i++;
        }
        return root;
    }

    @Override
    public String toString() {
        Queue<TreeNode> queue = new LinkedList<>();
        List<Integer> outputList = new ArrayList<>();
        queue.offer(this);
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node != null) {
                queue.offer(node.left);
                queue.offer(node.right);
                outputList.add(node.val);
            } else {
                outputList.add(null);
            }
        }
        while (!outputList.isEmpty() && outputList.get(outputList.size() - 1) == null) {
            outputList.remove(outputList.size() - 1);
        }
        return outputList.toString();
    }
}
