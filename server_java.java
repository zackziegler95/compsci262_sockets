import java.net.*;  
import java.io.*;  
import java.util.*;

class ServerJava{  
    // Translate to pig latin
    // from https://stackoverflow.com/questions/33403337/java-how-to-translate-a-string-to-piglatin
    public static String to_piglatin(String sentence) {
        sentence = sentence.replace(",", " ,");
        sentence = sentence.replace(".", " .");
        sentence = sentence.replace("!", " !");
        sentence = sentence.replace("?", " ?");

        List<Character> vowels = Arrays.asList('a', 'e', 'i', 'o', 'u');
        String[] words = sentence.split(" ");
        List<String> output_words = new ArrayList<>();

        for (String word : words) {
            int start = 0; // start index of word
            int firstVowel = 0;
            int end = word.length(); // end index of word
            for(int i = 0; i < end; i++) { // loop over length of word
                char c = Character.toLowerCase(word.charAt(i)); // char of word at i, lower cased
                System.out.println(c);
                if(vowels.contains(c)) { // convert vowels to a list so we can use List.contains() convenience method.
                    firstVowel = i;
                    break; // stop looping
                }
            }

            System.out.println(start+", "+firstVowel+", "+end);

            if(start != firstVowel) { // if start is not equal to firstVowel, we caught a vowel.
                String startString = word.substring(firstVowel, end);
                String endString = word.substring(start, firstVowel) + "ay";
                output_words.add(startString+endString);
            } else {
                output_words.add(word);
            }
        }
        
        sentence = String.join(" ", output_words);       
        sentence = sentence.replace(" ,", ",");
        sentence = sentence.replace(" .", ".");
        sentence = sentence.replace(" !", "!");
        sentence = sentence.replace(" ?", "?");
        return sentence;
    }

    public static void main(String args[])throws Exception{  
        ServerSocket ss=new ServerSocket(9000); // Both bind and listen
        Socket s=ss.accept(); // Accept is the same, returns a client socket

        // Here we're using Java's built in Data Streams to define a convention
        // that allows us to avoid looping
        DataInputStream din=new DataInputStream(s.getInputStream());  
        DataOutputStream dout=new DataOutputStream(s.getOutputStream());  
        
        // Java abstracts away the send and recv into file operations, hence read/write/flush
        String input = din.readUTF();
        System.out.println("client says: "+input);
        String output = to_piglatin(input);
        System.out.println("response : "+output);
        dout.writeUTF(output);
        dout.flush();

        din.close();  
        s.close();  
        ss.close();  
    }
    
}
