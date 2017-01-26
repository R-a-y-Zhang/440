(ns pathfinder.ipc.ipc
  (:gen-class))

(import (java.net URL HttpURLConnection)
        (java.io BufferedReader InputStreamReader OutputStream OutputStreamWriter))

(require '[clojure.data.json :as json])

(def new-session-url "http://localhost:5000/init_session")
(def setup-url "http://localhost:5000/setup")

(defn new-session
  []
  (println "Connecting to " new-session-url)
  (let [url (URL. new-session-url)
        conn (.openConnection url)]
    (.setRequestMethod conn "GET")
    (let [rd (BufferedReader. (InputStreamReader. (.getInputStream conn)))
          res (StringBuilder.)]
      (loop [line (.readLine rd)]
        (if-not (nil? line)
          (do (.append res line)
            (recur (.readLine rd)))
          (Integer/parseInt (.toString res)))))))

(defn flatten-array
  [a]
  (loop [array a res []]
    (if (zero? (count array))
      res
      (recur (rest array) (concat res (first array))))))

(defn setup-grid
  [sid array]
  (println sid setup-url)
  (let [height (count array)
        width (count (first array))
        flat-array (flatten-array array)
        jsonstr (json/write-str {:id sid :width width :height height :flattened_array flat-array})]
    (println jsonstr)
    (let [url (URL. setup-url)
          conn (.openConnection url)]
      (.setRequestMethod conn "POST")
      (.setDoOutput conn true)
      (.setRequestProperty conn "Content-Type" "application/json; charset=UTF-8")
      (let [wr (OutputStreamWriter. (.getOutputStream conn))]
        (.write wr jsonstr)
        (.flush wr)
        (.close wr))
      (let [rd (BufferedReader. (InputStreamReader. (.getInputStream conn)))
            res (StringBuilder.)]
        (loop [line (.readLine rd)]
          (if-not (nil? line)
            (do (.append res line)
              (recur (.readLine rd)))
            (.toString res)))))))

(defn spin-up
  [array]
  (let [id (new-session)]
    (setup-grid id array)))
