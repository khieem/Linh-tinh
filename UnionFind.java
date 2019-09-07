class UnionFind {
   private int[] parent;
   private int[] size;

   public UnionFind(int N) {
      parent = new int[N];
      size = new int[N];
      for (int i = 0; i < N; ++i) {
         parent[i] = i;
         size[i] = 1;
      }
   }

   public int root(int i) {
      while (i != parent[i]) {
         parent[i] = parent[parent[i]];
         i = parent[i];
      }
      return i;
   }

   public void union(int p, int q) {
      int pRoot = root(p);
      int qRoot = root(q);
      if (qRoot == pRoot) return;
      
      if (size[pRoot] < size[qRoot]) {
         parent[pRoot] = qRoot;
         size[qRoot] += size[pRoot];
      } else {
         parent[qRoot] = pRoot;
         size[pRoot] = qRoot;
      }
   }

   public void isConnected(int p, int q) {
      if (root(p) == root(q))
         System.out.println(p + " and " + q + " is connected!");
      else 
         System.out.println(p + " and " + q + " is NOT connected!");
   }

   public static void main(String[] args) {
      UnionFind uf = new UnionFind(11);
      uf.union(1, 5);
      uf.union(4, 7);
      uf.union(7, 9);
      uf.union(7, 8);
      uf.union(5, 4);
      uf.union(2, 6);
      uf.union(9, 6);
      uf.isConnected(6, 9);
   }
}