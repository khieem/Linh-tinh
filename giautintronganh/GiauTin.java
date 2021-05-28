import java.awt.image.BufferedImage;

public class GiauTin {

   private static int[] l = {0, 8, 16, 32, 64, 128};
	// private static int[] u = {7, 15, 31, 63, 127, 255};
	private static int[] w = {8, 8, 16, 32, 64, 128};
   private static int[][] R;

   private static int[][] normalize(int[][] img) throws Exception {
      for (int i = 0; i < img.length; i++) {
         for (int j = 0; j < img[0].length; j+=2) {
            int min = Math.min(img[i][j], img[i][j+1]);
            int max = Math.max(img[i][j], img[i][j+1]);
            
            if (min < 0) {
               img[i][j] += Math.abs(min);
               img[i][j+1] += Math.abs(min);
            }
            if (max > 255) {
               img[i][j] -= (max-255);
               img[i][j+1] -= (max-255);
            }
         }
      }
      return img;
   }
   public static void giau_tin(String path, String text, String key) throws Exception {
      String ciphertext = AES.encrypt(text, key);

		String ciphertext_bin = Utils.string_to_binary(ciphertext);
      int cipher_length = ciphertext_bin.length();
      String header = String.format("%10s", Integer.toBinaryString(cipher_length)).replaceAll(" ", "0");
      String secret = header + ciphertext_bin;
      // System.out.print(header);
      // System.out.println("co dc: "+secret);

      BufferedImage image = Utils.read_image(path);
		image = Utils.to_grayscale(image);
      int m = image.getHeight();
		int n = image.getWidth();

		int[][] img = Utils.image_to_matrix(image);

      // System.out.println("anh goc");
      // Main.print(img);/////////////////////////////////

      int[][] d = new int[m][n/2];
		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n/2; ++j) {
				d[i][j] = img[i][2*j+1] - img[i][2*j];
			}
		}

      R = new int[d.length][d[0].length];
		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n/2; ++j) {
				int di = Math.abs(d[i][j]);
				if      (di < 8)   R[i][j] = 1;
				else if (di < 16)  R[i][j] = 2;
				else if (di < 32)  R[i][j] = 3;
				else if (di < 64)  R[i][j] = 4;
				else if (di < 128) R[i][j] = 5;
				else if (di < 256) R[i][j] = 6;
			}
		}

		boolean stop = false;
		for (int i = 0; i < m && stop == false; ++i) {
			for (int j = 0; j < n/2 && stop == false; ++j) {
				// if (0 >= ciphertext_bin.length()) {
				// 	break;
				// }
	
				int k = (int) Math.floor(Math.log(w[R[i][j]-1]) / Math.log(2));
				String s = "";
				if (k >= secret.length()) {
					s = secret.substring(0);
               secret = "";
               stop = true;
               // break;
            }
				else {
					s = secret.substring(0, k);
               secret = new String(secret.substring(k));
					// start = start+k;
				}
				int b = Integer.parseInt(s, 2);
            
				// System.out.print(b + " ");
            // System.out.println(s);
            // System.out.println(ciphertext_bin);
				int di = 0;

				if (d[i][j] >= 0) {
					di = b + l[R[i][j]-1];
				} else {
					di = -(l[R[i][j]-1] + b);
				}
				
				float offset = (di-d[i][j])/2.f;
				if (d[i][j] % 2 == 0) {
					img[i][j*2] = img[i][j*2] - (int) Math.floor(offset);
					img[i][j*2+1] = img[i][j*2+1] + (int) Math.ceil(offset);
				} else {
					img[i][j*2] = img[i][j*2] - (int) Math.ceil(offset);
					img[i][j*2+1] = img[i][j*2+1] + (int) Math.floor(offset);
				}

		   }
      }
      // System.out.println("ma ttran giau");
      // Main.print(normalize(img));
      Utils.write_image(normalize(img));
      System.out.println("GIẤU THÔNG ĐIỆP THÀNH CÔNG");
      // image = Utils.read_image("kq.png");
		// img = Utils.image_to_matrix(image);
      // System.out.println("doc lai");
      // Main.print(img);
      // try {
      //    return normalize(img);
      // } catch (Exception e) {
      //    System.out.print(e.toString());
      // }
      // return null;
   }

   public static String tach_tin(String path, String key) {
      BufferedImage image = Utils.read_image(path);
		int[][] img = Utils.image_to_matrix(image);
      // System.out.println("doc lai");
      // Main.print(img);////////////////////////////
      int m = img.length;
      int n = img[0].length;
      String pad = "0";
      int[][] d1 = new int[m][n/2];
		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n/2; ++j) {
				d1[i][j] = Math.abs(img[i][2*j+1] - img[i][2*j]);
			}
		}

      int count = 0;
      boolean stop = false;
      boolean done = false;
      String header = "";
      int limit = 100;
      StringBuilder s = new StringBuilder();
      for (int i = 0; i < m && stop == false; ++i) {
         for (int j = 0; j < n/2 && stop == false; j+=1) {
            int k = (int) Math.floor(Math.log(w[R[i][j]-1]) / Math.log(2));
				int v = d1[i][j] - l[R[i][j]-1];
            if (count + k >= limit) {
               k = limit-count;
            }
            // System.out.print(v + " \n");
				// System.out.println(pad.repeat(k-Integer.toBinaryString(v).length()) + Integer.toBinaryString(v));
            String str;
            if (k > Integer.toBinaryString(v).length()) 
               str = pad.repeat(k-Integer.toBinaryString(v).length()) + Integer.toBinaryString(v);
            else
               str = Integer.toBinaryString(v);
            
            s.append(str);
            count += str.length();

            if (count >= limit) stop = true;
            // if (count + str.length() >= limit) {

            //    stop = true;
            // } else {
            //    s.append(str);
            //    count += str.length();
            // }
            if (s.length() >= 10 && done == false) {
               header = s.substring(0, 10);
               limit = Integer.parseInt(header, 2);
               s = s.delete(0, 10);
               count -= 10;
               done = true;
            }
			}
		}
      // System.out.println("co dc: " + ciphertext_length);
      // s.append(pad.repeat( (int) Math.ceil(s.length()/16.f)*16-s.length()));
      // return AES.decrypt(s.toString(), key);
      String c = Utils.binary_to_string(s.toString());
      return AES.decrypt(c, key);
   }
}
