public class loops { 
    public static void main(String[] args){

        int a = Integer.parseInt(args[0]);
        int b = Integer.parseInt(args[0]);

        //multiplication();
        Puissance(b);
        
    }

    public static void multiplication(int b ){
        for (int i = 0 ; i <= 10; i++){
            System.out.print( "\n" + "Table de" + i +":" + "\n");
            for (int j = 0 ; j <= 10; j++){
            System.out.print("\n" + i + "x" + j + "=" + i*j+ "\n");

            }
        }
    }

    public static void Puissance(int b ){
        long res=b;
        for (int i = 1 ; i <= 10; i++){
            res = res*b;
            System.out.println(b + " Puissance "+ i+" = "+res + "\n");    
        }
    }

}