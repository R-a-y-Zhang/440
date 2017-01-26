(ns pathfinder.core
  (:gen-class))

(require '[pathfinder.setup.setup :as setup])
(require '[pathfinder.ipc.ipc :as ipc])

(defn -main
  [& args]
  (ipc/spin-up (setup/randomize-terrain (setup/init-field 50 50) 50 50)))
