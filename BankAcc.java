import java.util.*;

class Work{
    Scanner scanf =new Scanner(System.in);
        String name;
        String add;
        int acn;
        int amt;
        void Deposite(){
            System.out.println("Enter the amount to be deposited :");
            int am=scanf.nextInt();
            if(am<0){
                System.out.println("Amount can not be negative!");
            } else{
            amt=amt+am;
            System.out.println("Amount deposited succesfully!");
            System.out.println("Your final Account Blance is :"+amt);
            }
        }
        void Withdraw(){
            System.out.println("Enter the amount to be withrawn :");
            int am=scanf.nextInt();
            if(am > amt){
                System.out.println("Your Account has not enough balance ):");
            } else if(am<0){
                System.out.println("Amount can not be negative!");
            } else {
            amt=amt-am;
            System.out.println("Amount withdrawn succesfully!");
            System.out.println("Your final Account Blance is :"+amt);
            }
        }
        void Display(){
                    System.out.println("Name :"+name);
                    System.out.println("Account number :"+acn);
                    System.out.println("Address :"+add);
                    System.out.println("Account Blance :"+amt);
        }
}
public class BankAcc{
        public static void main(String [] args){
            int ct=1;
            String st="ab";
            int ban=100001;
            Map<String,Work> map=new HashMap<>();
            while(ct==1){
            Scanner scanf =new Scanner(System.in);
            System.out.println("Welcome to Lena Dena Bank");
            System.out.println("press 1 :if you are a new customer \n press 2: if you are an existing customer \n Enter your chooice :");
            int cu=scanf.nextInt();
            if(cu==1){
                map.put(st,new Work());
                scanf.nextLine();
                System.out.println("Enter your name :");
                map.get(st).name = scanf.nextLine();
                scanf.nextLine();
                System.out.println("Enter your address :");
                map.get(st).add = scanf.nextLine();
                scanf.nextLine();
                System.out.println("Enter your opening amount:");
                map.get(st).amt = scanf.nextInt();
                map.get(st).acn = ban;
                System.out.println("Your uniqe Cumstomer I'd is :"+st+"\n keep it for your further refrences!");
                ban++;
                char[] charArray = st.toCharArray();
                char fl='a';
                int inc=0;
                if(fl=='z'){
                    inc++;
                }
                 fl = charArray[inc];
                fl++; 
                charArray[inc] = fl;
                st = new String(charArray);
            } else if(cu==2){
                        System.out.println("Press 1: To deposite \nPress 2: To withdraw \n Press 3: To display details \n Enter your choice : ");
                      int ch=scanf.nextInt();
                      switch (ch) {
                          case 1:{
                            System.out.println("Enter your uniqe customer I'd :");
                            String ci=scanf.next();
                            map.get(ci).Deposite();
                            break;
                          }
                         case 2:{
                            System.out.println("Enter your uniqe customer I'd :");
                            String ci=scanf.next();
                            map.get(ci).Withdraw();
                            break;
                         } 
                         case 3:{
                            System.out.println("Enter your uniqe customer I'd :");
                            String ci=scanf.next();
                            map.get(ci).Display();
                            break;
                         }
                        default :{
                            System.out.println("Enter a valid option!");
                        }
                      }
            } else{
                System.out.println("Enter a valid input :");
                cu=scanf.nextInt();
            }
            System.out.println("Press 1: To run the code again.\nPress 2: to exit.\n Enter your chooice :");
            ct=scanf.nextInt();
            if(ct<=0 || ct>=3){
                System.out.println("Enter a valid option!:");
                ct=scanf.nextInt();
            }
        }
        }
}