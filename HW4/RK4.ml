(* let ( |> ) x f = f x *)

let m = ref 0.1
let beta = ref 0.0
let l = ref 0.1
let g = ref 9.8
let a = ref 0.0
let alpha = ref 0.0


let ( *** ) scale vector =
	(* scale a vector with scaling value*)
	List.map (fun x -> scale*.x) vector

let  ( ++ ) xs ys = 
	(* vector additioon *)
	List.combine xs ys |>
	List.map (fun (x,y) -> x +. y)

let f_vector fs vector t = 
	(* This imitates f(x,t) *)
	List.map (fun f -> f vector t) fs

let f1_pendulum vector t =
	(* vector[0] should be theta and  vector[1] should be omega *)
	List.nth vector 1

let f2_pendulum vector t = 
	(* vector[0] should be theta and  vector[1] should be omega *)
	let theta = List.nth vector 0 in
	let omega = List.nth vector 1 in
	let first = ~-.(!beta /. !m) *. omega in 
	let second = ~-.(!g /. !l) *. (sin theta) in
	let third = (!a/.(!m *. !l)) *.(cos !alpha *. t) in 
	first +. second +. third

let rec rk4_solver fs x t h n =
	if n = 0 
		then ()
	else
		let f = f_vector fs in 
		let k1 = h *** (f x t) in
		let k2 = h *** (f (x ++ (0.5 *** k1)) (t +. h/.2.0) ) in
		let k3 = h *** (f (x ++ (0.5 *** k2)) (t +. h/.2.0) ) in
		let k4 = h *** (f (x ++ k3) (t +. h) ) in
		let x_t_h = x ++ (1.0/.6.0) *** (k1 ++ (2.0 *** k2) ++ (2.0 *** k3) ++ k4) in
		Printf.printf "x_%f,%f,%f\n" (t +. h) (List.nth x_t_h 0) (List.nth x_t_h 1);
		rk4_solver fs x_t_h (t +. h) h (n - 1)




let main () =
	let t0 = float_of_string Sys.argv.(1) in 
	let dt = float_of_string Sys.argv.(2) in
	let n  = int_of_string Sys.argv.(3) in
	let theta = float_of_string Sys.argv.(4) in
	let omega = float_of_string Sys.argv.(5) in
	let x0 = [theta; omega] in
	rk4_solver [f1_pendulum; f2_pendulum] x0 t0 dt n

let () = main ()

