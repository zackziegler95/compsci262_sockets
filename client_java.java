import java.net.*;  
import java.io.*;  

class ClientJava{  
    public static void main(String args[])throws Exception{  
        Socket s=new Socket("localhost", 9000); // As usual we start off with a client socket

        // Like the server, we're using streams to define a good convention
        DataInputStream din=new DataInputStream(s.getInputStream());  
        DataOutputStream dout=new DataOutputStream(s.getOutputStream());  
        
        // ez
        String text = "Hello, world";
        dout.writeUTF(text);
        dout.flush();

        String response = din.readUTF();

        System.out.println(response);  
          
        dout.close();  
        s.close();  
    }
}
