class Percolation {
   private int[] parent;
   private int[] size;
   private static int top;
   private static int bottom;

   public Percolation(int N) {
      parent = new int[N];
      size = new int[N];
      for (int i = 0; i < N; ++i) {
         parent[i] = i;
         size[i] = 1;
      }

      top = 0;
      bottom = N-1;

      for (int i = 0; i < Math.sqrt(N); ++i) 
         union(top, i);

      for (int j = N - (int) Math.sqrt(N); j < N; ++j)
         union(bottom, j);
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

   public void connected(int p, int q) {
      if (root(p) == root(q))
         System.out.println("Percolate!");
      else 
         System.out.println("NOT percolate!");
   }

   public static void main(String[] args) {
      Percolation pc = new Percolation(25);
      pc.union(4, 9);
      pc.union(2, 7);
      pc.union(7, 12);
      pc.union(7, 6);
      pc.union(5, 6);
      pc.union(5, 10);
      pc.union(19, 18);
      pc.connected(pc.top, pc.bottom);
   }
}