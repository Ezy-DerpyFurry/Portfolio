import qualified Data.Map as Map
import Data.Char (toLower)

main :: IO ()
main = do
    putStrLn "Hello, World! (From haskell)"
    loop

responses :: Map.Map String String
responses = Map.fromList [("hi", "Hello!"), ("bye", "Why are you leaving?")]

loop :: IO ()
loop = do
    putStr "Say Hi: "
    msg <- getLine
    let msgLower = map toLower msg

    if msgLower == "quit" then
        putStrLn "See you later!"
    else
        case Map.lookup msgLower responses of
            Just reply -> do
                putStrLn reply
                loop
            Nothing -> do
                putStrLn "I don't understand what you mean."
                loop

