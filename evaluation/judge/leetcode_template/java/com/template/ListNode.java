package com.template;

import java.util.ArrayList;
import java.util.List;

public class ListNode {
    public int val;
    public ListNode next;

    // Constructor
    public ListNode(int val) {
        this.val = val;
        this.next = null;
    }

    public ListNode(int val, ListNode next) {
        this.val = val;
        this.next = next;
    }

    // toString method using List<Integer>
    @Override
    public String toString() {
        List<Integer> outputList = new ArrayList<>();
        ListNode p = this;
        while (p != null) {
            outputList.add(p.val);
            p = p.next;
        }
        return outputList.toString();
    }

    // Static method to construct ListNode from an array
    public static ListNode constructListNodeFromList(List<Integer> data) {
        if (data == null || data.isEmpty()) {
            return null;
        }
        ListNode head = new ListNode(data.get(0)); // Use get() to access the first element
        ListNode p = head;
        for (int i = 1; i < data.size(); i++) { // Use size() for list length and get() to access elements
            p.next = new ListNode(data.get(i));
            p = p.next;
        }
        return head;
    }
}
