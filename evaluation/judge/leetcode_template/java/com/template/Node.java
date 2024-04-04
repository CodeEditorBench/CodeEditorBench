package com.template;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Node {
    public int val;
    public List<Node> neighbors;

    // Constructor
    public Node(int val) {
        this.val = val;
        this.neighbors = new ArrayList<>();
    }

    public Node(int val, List<Node> neighbors) {
        this.val = val;
        this.neighbors = neighbors != null ? new ArrayList<>(neighbors) : new ArrayList<>();
    }

    // toString method to display Node and its neighbors as a string
    @Override
    public String toString() {
        List<Node> nodeList = new ArrayList<>();
        nodeList.add(this);
        List<Integer> outputList = new ArrayList<>();
        while (!nodeList.isEmpty()) {
            Node node = nodeList.remove(0);
            if (node != null) {
                nodeList.addAll(node.neighbors);
                outputList.add(node.val);
            } else {
                outputList.add(null); // Assuming 'None' is represented as null in Java
            }
        }
        return outputList.toString();
    }

    // Static method to construct Node from a list of list
    public static Node constructNodeFromList(List<List<Integer>> data) {
        if (data == null || data.isEmpty()) {
            return null;
        }

        Map<Integer, Node> nodeMap = new HashMap<>();
        Node root = null;

        for (List<Integer> pair : data) {
            Node node;
            if (!nodeMap.containsKey(pair.get(0))) {
                node = new Node(pair.get(0));
                nodeMap.put(pair.get(0), node);
                if (root == null) {
                    root = node; // The first node is considered as root
                }
            } else {
                node = nodeMap.get(pair.get(0));
            }

            for (int i = 1; i < pair.size(); i++) {
                Node neighbor;
                if (nodeMap.containsKey(pair.get(i))) {
                    neighbor = nodeMap.get(pair.get(i));
                } else {
                    neighbor = new Node(pair.get(i));
                    nodeMap.put(pair.get(i), neighbor);
                }
                node.neighbors.add(neighbor);
            }
        }
        return root;
    }
}
