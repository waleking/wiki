package dev.weijing.wiki;

import java.util.regex.Pattern;
import java.util.regex.Matcher;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.io.PrintStream;

import info.bliki.wiki.model.WikiModel;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.WikiXMLParser;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.filter.PlainTextConverter;

public class BlikiExample {

    public static void main(String[] args) throws Exception {
        String dumpfile = args[0];

        IArticleFilter handler = new ArticleFilter();
        WikiXMLParser wxp = new WikiXMLParser(new File(dumpfile), handler);

        wxp.parse();
    }

    /**
     * Print title an content of all the wiki pages in the dump.
     *
     */
	static class ArticleFilter implements IArticleFilter {

		final static Pattern regex = Pattern.compile("[A-Z][\\p{L}\\w\\p{Blank},\\\"\\';\\[\\]\\(\\)-]+[\\.!]",
				Pattern.CANON_EQ);

		// Convert to plain text
		WikiModel wikiModel = new WikiModel("${image}", "${title}");

		public void process(WikiArticle page, Siteinfo siteinfo)  throws IOException{

			if (page != null && page.getText() != null && !page.getText().startsWith("#REDIRECT ")){

				PrintStream out = null;

				try {
					out = new PrintStream(System.out, true, "UTF-8");
				} catch (UnsupportedEncodingException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

				// Zap headings ==some text== or ===some text===

				// <ref>{{Cite web|url=http://tmh.floonet.net/articles/falseprinciple.html |title="The False Principle of our Education" by Max Stirner |publisher=Tmh.floonet.net |date= |accessdate=2010-09-20}}</ref>
				// <ref>Christopher Gray, ''Leaving the Twentieth Century'', p. 88.</ref>
				// <ref>Sochen, June. 1972. ''The New Woman: Feminism in Greenwich Village 1910?1920.'' New York: Quadrangle.</ref>

				// String refexp = "[A-Za-z0-9+\\s\\{\\}:_=''|\\.\\w#\"\\(\\)\\[\\]/,?&%?-]+";
				String wikiTitle=page.getTitle();
				//out.println("===="+wikiTitle);

				String wikiText = page.getText().
									replaceAll("[=]+[A-Za-z+\\s-]+[=]+", " ").
									replaceAll("\\{\\{[A-Za-z0-9+\\s-]+\\}\\}"," ").
									replaceAll("(?m)<ref>.+</ref>"," ").
									replaceAll("(?m)<ref name=\"[A-Za-z0-9\\s-]+\">.+</ref>"," ").
									replaceAll("<ref>"," <ref>");

				// Remove text inside {{ }}
				try {
					String plainStr = wikiModel.render(new PlainTextConverter(), wikiText).
							replaceAll("\\{\\{[A-Za-z+\\s-]+\\}\\}", " ");
					Matcher regexMatcher = regex.matcher(plainStr);
					StringBuffer sb=new StringBuffer();
					while (regexMatcher.find())
					{
						// Get sentences with 1 or more words
						String sentence = regexMatcher.group();

						if (matchSpaces(sentence, 1)) {
							//out.println(sentence);
							sb.append(sentence+" ");
						}
					}
					String wikiContent=sb.toString();
					if(wikiContent.length()!=0){
                        System.out.println(wikiTitle+"\t"+wikiContent);
					}else{
						//System.out.println(wikiTitle+" is not a page");
					}
				}catch (IOException e){
					throw e;
				}

			}
		}

		private boolean matchSpaces(String sentence, int matches) {

			int c =0;
			for (int i=0; i< sentence.length(); i++) {
				if (sentence.charAt(i) == ' ') c++;
				if (c == matches) return true;
			}
			return false;
		}

	}


}
