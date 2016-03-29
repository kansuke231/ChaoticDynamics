
(* coefficients for Lorenz system *)
let a = 16.0
let r = 45.0
let b = 4.0


(* coefficients for Rossler system 
let a = 0.398
let b = 2.0
let c = 4.0
*)
let c = 4.0
(* for adaptive RK4 *)
let error = 100.0


let ( *** ) scale vector =
	(* scale a vector with scaling value*)
	List.map (fun x -> scale*.x) vector

let  ( ++ ) xs ys = 
	(* vector additioon *)
	List.combine xs ys |>
	List.map (fun (x,y) -> x +. y)

let  ( -- ) xs ys = 
	(* vector subtraction *)
	List.combine xs ys |>
	List.map (fun (x,y) -> x -. y)

let rec inf_norm l = 
	(* infinite norm *)
	match l with
	| [] -> 0.0
  	| h :: t -> max (abs_float h) (abs_float (inf_norm t))

let f_vector fs vector t = 
	(* This imitates f(x,t) *)
	List.map (fun f -> f vector t) fs

(*-----------------------------------------*)
let f1_lorenz vector t =
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	a *. (y-.x)

let f2_lorenz vector t =
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	let z = List.nth vector 2 in
	(r*.x) -. y -. (x*.z)

let f3_lorenz vector t =
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	let z = List.nth vector 2 in
	(x *. y) -. (b*.z)
(*-----------------------------------------*)

let f1_rossler vector t =
	let y = List.nth vector 1 in
	let z = List.nth vector 2 in
	~-.(y +. z)

let f2_rossler vector t =
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	x +. (a *. y)

let f3_rossler vector t =
	let x = List.nth vector 0 in
	let z = List.nth vector 2 in
	b +. (z*.(x -. c))


(*-----------------------------------------*)

let rec rk4_solver fs x t h n = 
	if n = 0 then 
		x
	else
		let f = f_vector fs in 
		let k1 = h *** (f x t) in
		let k2 = h *** (f (x ++ (0.5 *** k1)) (t +. h/.2.0) ) in
		let k3 = h *** (f (x ++ (0.5 *** k2)) (t +. h/.2.0) ) in
		let k4 = h *** (f (x ++ k3) (t +. h) ) in
		let x_t_h = x ++ (1.0/.6.0) *** (k1 ++ (2.0 *** k2) ++ (2.0 *** k3) ++ k4) in
		rk4_solver fs x_t_h (t +. h) h (n - 1)

let rec rk4_non_adaptive fs x t h n =
	if n = 0 
		then ()
	else
		let f = f_vector fs in 
		let k1 = h *** (f x t) in
		let k2 = h *** (f (x ++ (0.5 *** k1)) (t +. h/.2.0) ) in
		let k3 = h *** (f (x ++ (0.5 *** k2)) (t +. h/.2.0) ) in
		let k4 = h *** (f (x ++ k3) (t +. h) ) in
		let x_t_h = x ++ (1.0/.6.0) *** (k1 ++ (2.0 *** k2) ++ (2.0 *** k3) ++ k4) in
		Printf.printf "x_%f,%f,%f,%f\n" (t +. h) (List.nth x_t_h 0) (List.nth x_t_h 1) (List.nth x_t_h 2);
		rk4_non_adaptive fs x_t_h (t +. h) h (n - 1)

let rec rk4_adaptive fs x t h n = 
	if n = 0 then 
		()
	else 
	(
		let x1_t_h = rk4_solver fs x t h 1 in
		let x2_t_h = rk4_solver fs x t (h/.2.0) 2 in
		let delta1 = inf_norm (x1_t_h -- x2_t_h) in

		if delta1 > error then
			rk4_adaptive fs x t (h/.2.0) n
		else 
		(
			 let x1_t_2h = rk4_solver fs x t h 2 in 
			 let x2_t_2h = rk4_solver fs x t (2.0*.h) 1 in
			 let delta2 = inf_norm (x1_t_2h -- x2_t_2h) in 

			 if delta2 > error then
			 (
			 	Printf.printf "x_%f,%f,%f,%f\n" (t +. h) (List.nth x2_t_h 0) (List.nth x2_t_h 1) (List.nth x2_t_h 2); 
			 	rk4_adaptive fs x2_t_h (t+.h) h (n-1)
			 )
			 else 
			 (
			 	let double_h = 2.0*.h in 
			 	Printf.printf "x_%f,%f,%f,%f\n" (t +. double_h) (List.nth x1_t_2h 0) (List.nth x1_t_2h 1) (List.nth x1_t_2h 2);
			 	rk4_adaptive fs x1_t_2h (t +. double_h) double_h (n-1)
			 )
		)
	)

let main () =
	let t0 = float_of_string Sys.argv.(1) in 
	let dt = float_of_string Sys.argv.(2) in
	let n = int_of_string Sys.argv.(3) in
	let x = float_of_string Sys.argv.(4) in
	let y = float_of_string Sys.argv.(5) in
	let z = float_of_string Sys.argv.(6) in
	let x0 = [x; y; z] in
	Printf.printf "x_%f,%f,%f,%f\n" t0 x y z;
	rk4_non_adaptive [f1_lorenz; f2_lorenz; f3_lorenz] x0 t0 dt n

let () = main ()

