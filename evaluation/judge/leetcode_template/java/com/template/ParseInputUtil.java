package com.template;

import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class ParseInputUtil {
    private static final Gson gson = new Gson();

    public static boolean parseBool(String inputStr) {
        return gson.fromJson(inputStr, Boolean.class);
    }

    public static float parseFloat(String inputStr) {
        return gson.fromJson(inputStr, Float.class);
    }

    public static int parseInt(String inputStr) {
        return gson.fromJson(inputStr, Integer.class);
    }

    public static String parseStr(String inputStr) {
        return gson.fromJson(inputStr, String.class);
    }

    public static ListNode parseListNode(String inputStr) {
        Type listType = new TypeToken<List<Integer>>(){}.getType();
        List<Integer> dataList = gson.fromJson(inputStr, listType);
        return ListNode.constructListNodeFromList(dataList); 
    }

    public static TreeNode parseTreeNode(String inputStr) {
        Type listType = new TypeToken<List<Integer>>(){}.getType();
        List<Integer> dataList = gson.fromJson(inputStr, listType);
        return TreeNode.constructTreeNodeFromList(dataList); 
    }

    public static Node parseNode(String inputStr) {
        Type listType = new TypeToken<List<List<Integer>>>(){}.getType();
        List<List<Integer>> dataList = gson.fromJson(inputStr, listType);
        return Node.constructNodeFromList(dataList); 
    }

    public static List<Boolean> parseListOfBool(String inputStr) {
        Type listType = new TypeToken<List<Boolean>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<Float> parseListOfFloat(String inputStr) {
        Type listType = new TypeToken<List<Float>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<Integer> parseListOfInt(String inputStr) {
        Type listType = new TypeToken<List<Integer>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<String> parseListOfStr(String inputStr) {
        Type listType = new TypeToken<List<String>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<ListNode> parseListOfListNode(String inputStr) {
        Type listType = new TypeToken<List<List<Integer>>>(){}.getType();
        List<List<Integer>> dataList = gson.fromJson(inputStr, listType);
        List<ListNode> result = new ArrayList<>();
        for (List<Integer> data : dataList) {
            result.add(ListNode.constructListNodeFromList(data));
        }
        return result;
    }

    public static List<TreeNode> parseListOfTreeNode(String inputStr) {
        Type listType = new TypeToken<List<List<Integer>>>(){}.getType();
        List<List<Integer>> dataList = gson.fromJson(inputStr, listType);
        List<TreeNode> result = new ArrayList<>();
        for (List<Integer> data : dataList) {
            result.add(TreeNode.constructTreeNodeFromList(data));
        }
        return result;
    }

    public static List<Node> parseListOfNode(String inputStr) {
        Type listType = new TypeToken<List<List<List<Integer>>>>(){}.getType();
        List<List<List<Integer>>> dataList = gson.fromJson(inputStr, listType);
        List<Node> result = new ArrayList<>();
        for (List<List<Integer>> data : dataList) {
            result.add(Node.constructNodeFromList(data));
        }
        return result;
    }

    public static List<List<Integer>> parseListOfListOfBool(String inputStr) {
        Type listType = new TypeToken<List<List<Boolean>>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<List<Integer>> parseListOfListOfInt(String inputStr) {
        Type listType = new TypeToken<List<List<Integer>>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<List<Float>> parseListOfListOfFloat(String inputStr) {
        Type listType = new TypeToken<List<List<Float>>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    public static List<List<String>> parseListOfListOfStr(String inputStr) {
        Type listType = new TypeToken<List<List<String>>>(){}.getType();
        return gson.fromJson(inputStr, listType);
    }

    // 解析字符串到指定类型的对象
    public static Object parseStringToType(String stringParam, Type paramType) {
        if (Boolean.class == paramType || boolean.class == paramType) {
            return parseBool(stringParam);
        } else if (Float.class == paramType || float.class == paramType) {
            return parseFloat(stringParam);
        } else if (Integer.class == paramType || int.class == paramType) {
            return parseInt(stringParam);
        } else if (String.class == paramType) {
            return parseStr(stringParam);
        } else if (ListNode.class == paramType) {
            return parseListNode(stringParam);
        } else if (TreeNode.class == paramType) {
            return parseTreeNode(stringParam);
        } else if (Node.class == paramType) {
            return parseNode(stringParam);
        } else if (int[].class == paramType) {
            return gson.fromJson(stringParam, int[].class);
        } else if (Integer[].class == paramType) {
            return gson.fromJson(stringParam, Integer[].class);
        } else if (String[].class == paramType) {
            return gson.fromJson(stringParam, String[].class);
        } else if (boolean[].class == paramType) {
            return gson.fromJson(stringParam, boolean[].class);
        } else if (Boolean[].class == paramType) {
            return gson.fromJson(stringParam, Boolean[].class);
        } else if (float[].class == paramType) {
            return gson.fromJson(stringParam, float[].class);
        } else if (Float[].class == paramType) {
            return gson.fromJson(stringParam, Float[].class);
        } else if (TreeNode[].class == paramType) {
            List<TreeNode> list = parseListOfTreeNode(stringParam);
            return list.toArray(new TreeNode[0]);
        } else if (Node[].class == paramType) {
            List<Node> list = parseListOfNode(stringParam);
            return list.toArray(new Node[0]);
        } else if (ListNode[].class == paramType) {
            List<ListNode> list = parseListOfListNode(stringParam);
            return list.toArray(new ListNode[0]);
        } else if (int[][].class == paramType) {
            return gson.fromJson(stringParam, int[][].class);
        } else if (Integer[][].class == paramType) {
            return gson.fromJson(stringParam, Integer[][].class);
        } else if (String[][].class == paramType) {
            return gson.fromJson(stringParam, String[][].class);
        } else if (boolean[][].class == paramType) {
            return gson.fromJson(stringParam, boolean[][].class);
        } else if (Boolean[][].class == paramType) {
            return gson.fromJson(stringParam, Boolean[][].class);
        } else if (float[][].class == paramType) {
            return gson.fromJson(stringParam, float[][].class);
        } else if (Float[][].class == paramType) {
            return gson.fromJson(stringParam, Float[][].class);
        } else if (paramType instanceof ParameterizedType) {
            // 解析泛型类型的参数
            ParameterizedType parameterizedType = (ParameterizedType) paramType;
            Type rawType = parameterizedType.getRawType();
            if (List.class == rawType) {
                Type[] typeArguments = parameterizedType.getActualTypeArguments();
                if (typeArguments.length == 1) {
                    Class<?> typeArgClass = (Class<?>) typeArguments[0];
                    if (Boolean.class == typeArgClass || boolean.class == typeArgClass) {
                        return parseListOfBool(stringParam);
                    } else if (Float.class == typeArgClass || float.class == typeArgClass) {
                        return parseListOfFloat(stringParam);
                    } else if (Integer.class == typeArgClass || int.class == typeArgClass) {
                        return parseListOfInt(stringParam);
                    } else if (String.class == typeArgClass) {
                        return parseListOfStr(stringParam);
                    } else if (ListNode.class == typeArgClass) {
                        return parseListOfListNode(stringParam);
                    } else if (TreeNode.class == typeArgClass) {
                        return parseListOfTreeNode(stringParam);
                    } else if (Node.class == typeArgClass) {
                        return parseListOfNode(stringParam);
                    } else if (List.class.isAssignableFrom(typeArgClass)) {
                        // 解析List<List<Integer>>这种类型的参数
                        Type[] typeArguments2 = ((ParameterizedType) typeArguments[0]).getActualTypeArguments();
                        if (typeArguments2.length == 1) {
                            Class<?> typeArgClass2 = (Class<?>) typeArguments2[0];
                            if (Integer.class == typeArgClass2 || int.class == typeArgClass2) {
                                return parseListOfListOfInt(stringParam);
                            } else if (Float.class == typeArgClass2 || float.class == typeArgClass2) {
                                return parseListOfListOfFloat(stringParam);
                            } else if (String.class == typeArgClass2) {
                                return parseListOfListOfStr(stringParam);
                            } else if (Boolean.class == typeArgClass2) {
                                return parseListOfListOfBool(stringParam);
                            }
                        }
                    }
                }
            }
        }

        throw new IllegalArgumentException("Unsupported parameter type: " + paramType);
    }
}
