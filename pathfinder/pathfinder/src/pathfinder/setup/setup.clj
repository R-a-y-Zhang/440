(ns pathfinder.setup.setup
  (:gen-class))

(defn repeat-array
  [array n]
  (loop [res [] i 0]
    (if (= i n)
      res
      (recur (conj res array) (inc i)))))

(defn init-field
  ([w h]
   (init-field w h 1))
  ([w-size h-size v] ;; w width, h height
   (let [w (vec (repeat w-size v))]
     (repeat-array w h-size))))

(defn add-rivers
  [array]
  array)

(defn randomize-heights
  [width height]
  (loop [w width h width buff [] arr []]
    (let [wrand (fn [] (vec (take width (repeatedly #(if (< (rand) 0.5) 1 0)))))]
      (vec (take height (repeatedly wrand))))))

(defn merge-row
  [row1 row2 s]
  (if (<= (+ (count row2) s) (count row1))
    (loop [r1 row1 r2 row2 s1 0]
      (if (zero? (count r2))
        r1
        (let [pos (+ s1 s)
              v1 (nth r1 pos)
              v2 (first r2)]
          (recur (assoc r1 pos (+ v1 v2)) (rest r2) (inc s1)))))))

(defn merge-arrays
  [array1 array2 w1 h1]
    (loop [arr1 array1 arr2 array2 h 0]
      (if (zero? (count arr2))
        arr1
        (let [hh (+ h1 h)
              row1 (nth arr1 hh)
              row2 (first arr2)
              nrow (merge-row row1 row2 w1)]
          (recur (assoc arr1 hh nrow) (rest arr2) (inc h))))))

(defn randomize-terrain
  [array width height]
  (let [wbounds (- width 31)
        hbounds (- height 31)
        w (rand-int wbounds)
        h (rand-int hbounds)
        mod-array (randomize-heights w h)]
    (merge-arrays array mod-array w h)))

(defn iterative-randomize
  [a n]
  (loop [array a s n]
    (if (zero? s)
      array
      (recur (randomize-terrain array (count array) (count (first array))) (dec s)))))

(defn render-terrain
  [array]
    (add-rivers (iterative-randomize array 8)))


