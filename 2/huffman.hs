import qualified Data.Map as M
import Data.List (sortBy, intercalate)
import Data.Function (on)

countChars text = sortBy sndDescSort $ M.toList $ M.fromListWith (+) [(c, 1) | c <- text]
  where sndDescSort = flip compare `on` snd

data Tree = Branch Tree Tree
          | Leaf Char Integer
          deriving (Show)

weight :: Tree -> Integer
weight (Leaf _ w)   = w
weight (Branch x y) = weight x + weight y

buildTree :: [Tree] -> Tree
buildTree [x] = x
buildTree xs = buildTree $ Branch x y : rest
  where ([x,y], rest) = splitAt 2 $ sortBy (compare `on` weight) xs

codify :: Tree -> M.Map Char String
codify = helper ""
  where helper prefix (Leaf c _) = M.singleton c prefix
        helper prefix (Branch x y) =
          M.union
            (helper (prefix ++ "0") x)
            (helper (prefix ++ "1") y)

encode :: M.Map Char String -> String -> String
encode code = concatMap (code M.!)

entropy source = sum $ map (f . ((/ fromIntegral total) . fromIntegral) . snd) $ countChars source
  where total = length source
        f x = -x * logBase 2 x

main = do
  text <- readFile "Alice29.txt"
  let dist   = countChars text
      tree   = buildTree $ map (uncurry Leaf) dist
      code   = codify tree
      result = encode code text
  putStrLn $ latexTable dist code
  print $ length result
  print $ fromIntegral (length result) / fromIntegral (length text)
  print $ fromIntegral (length result) / fromIntegral (length text * 8)
  print $ entropy text
  putStrLn $ take 200 result

latexTable dist code = intercalate "\n" $ map format dist
  where format :: (Char, Integer) -> String
        format (a, b) = escape (show a) ++ "\t&\t" ++ show b ++ "\t&\t" ++ code M.! a ++ "\t\\\\"
        escape :: String -> String
        escape ('\\':xs) = "\\textbackslash " ++ escape xs
        escape ('_':xs) = "\\_" ++ escape xs
        escape (x:xs)    = x : escape xs
        escape []        = []

