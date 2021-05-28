public class Main {
	public static void print(int m[][]) {
		for (int[] row : m) {
			for (int element : row)
				System.out.printf("%5d", element);
			System.out.println();
		}
	}

	public static void main(String[] args) throws Exception {
		
		String plaintext = "abcmutnrtbde";
		final String key = "3e3";

		
	// 	// String raw = Arrays.stream(a.split(" ")).map(binary -> Integer.parseInt(binary, 2))
	// 	//                 .map(Character::toString)
	// 	//                 .collect(Collectors.joining());
	// 	// System.out.println(raw);
		
		String path = "C:\\Users\\khieem\\OneDrive\\Hình ảnh\\177708_126413164163198_563416135_o.jpg";
		// String path = "C:\\Users\\khieem\\Downloads\\IMG_20210328_083853.jpg";
		// String path = "C:\\Users\\khieem\\Downloads\\OIP.jpeg";

		try {
			GiauTin.giau_tin(path, plaintext, key);
		} catch (Exception e) {
			System.out.print("chon anh khac");
		}
	
		System.out.println("-----------------------------");

		String anh_giau_tin = "kq.png";
		System.out.println("THÔNG ĐIỆP GIẤU TRONG ẢNH: " + GiauTin.tach_tin(anh_giau_tin, key));
	}
}