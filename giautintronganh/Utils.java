import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import javax.imageio.ImageIO;

import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;
import java.io.IOException;

public class Utils {
	static int KEY_SIZE = 16;
	// private static String to_decimal(String s) throws Exception {
	// 	int n = s.length();
	// 	if (n > KEY_SIZE)
	// 		 throw new Exception("thông điệp dài tối đa 16 kí tự");

	// 	StringBuilder sb = new StringBuilder();
	// 	for (int i = 0; i < n; ++i)
	// 		 sb.append((byte) s.charAt(i) + " ");
	// 	String pad = "32 ";
	// 	sb.append(pad.repeat(KEY_SIZE-n));
	// 	return sb.toString().strip();
	// }

	public static String string_to_binary(String input) {
			StringBuilder result = new StringBuilder();
			char[] chars = input.toCharArray();
			for (char c : chars)
				result.append(String.format("%8s", Integer.toBinaryString(c)).replaceAll(" ", "0"));
			return result.toString();

	}

	public static String binary_to_string(String bin) {
		StringBuilder s = new StringBuilder();
		for (int i = 0; i < bin.length(); i+=8) {
			String temp = bin.substring(i, i+8);
			int num = Integer.parseInt(temp,2);
			char letter = (char) num;
			s.append(letter);
		}
		return s.toString();
	}
	public static String tach_ra_cho_de_doc(String s, int block_size, String separator) {
			List<String> result = new ArrayList<>();
			int index = 0;
			while (index < s.length()) {
				result.add(s.substring(index, Math.min(index + block_size, s.length())));
				index += block_size;
			}
			return result.stream().collect(Collectors.joining(separator));
	}

	public static BufferedImage read_image(String path) {
		File file = new File(path);
		BufferedImage image = null;
		try {
			image = ImageIO.read(file);
		}
		catch (IOException e) { System.out.println("hi"); }
		return image;
	}

	public static BufferedImage to_grayscale(BufferedImage image) {
		int width = image.getWidth();
		int height = image.getHeight();

		for (int y = 0; y < height; ++y) {
			for (int x = 0; x < width; ++x) {
				int p = image.getRGB(x, y);

				int a = (p>>24) & 0xff;
				int r = (p>>16) & 0xff;
				int g = (p>>8) & 0xff;
				int b = p & 0xff;

				int avg = (r+g+b) / 3;
				p = (a<<24) | (avg<<16) | (avg<<8) | avg;
				image.setRGB(x, y, p);
			}
		}
		return image;
	}

	public static int[][] image_to_matrix(BufferedImage image) {
		int m = image.getHeight();
		int n = image.getWidth();
		int[][] kq = new int[m][n];
		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n; ++j) {
				int p = image.getRGB(j, i);
				kq[i][j] = (p>>16) & 0xff;
			}
		}
		return kq;
	}

	public static void write_image(int[][] matrix) {
		int m = matrix.length;
		int n = matrix[0].length;
		BufferedImage image = new BufferedImage(n, m, BufferedImage.TYPE_4BYTE_ABGR);
		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n; j++) {
					int a = matrix[i][j];
					Color newColor = new Color(a,a,a);
					image.setRGB(j, i, newColor.getRGB());
			}
		}
		File output = new File("kq.png");
		try {
			ImageIO.write(image, "png", output);
		}
		catch (Exception e) {}
	}

	public static int min(int[][] a) {
		int min = a[0][0];
		for (int[] row : a)
			for (int x : row) 
				if (min > x) min = x;
		return min;
	}

	public static int max(int[][] a) {
		int max = a[0][0];
		for (int[] row : a)
			for (int x : row) 
				if (max < x) max = x;
		return max;
	}
}
// 010010000011100001110000010100110011100101000101001100010111001101101111010001000110101100110000011010010110001101010100001100000100010001001100010100000100000101000110010100010011110100111101