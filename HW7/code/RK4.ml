
(* coefficients for Lorenz system *)
let a = 16.0
let r = 45.0
let b = 4.0


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

(*-------------------------------------------------------------------------------------*)
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
(*-------------------------------------------------------------------------------------*)

let d'_xx vector t = 
	let d_xx = List.nth vector 3 in
	let d_xy = List.nth vector 4 in
	a*.(d_xy -. d_xx)

let d'_xy vector t = 
	let x = List.nth vector 0 in
	let z = List.nth vector 2 in
	let d_xx = List.nth vector 3 in
	let d_xy = List.nth vector 4 in
	let d_xz = List.nth vector 5 in
	(r -. z)*.d_xx -. d_xy -. x*.d_xz

let d'_xz vector t = 
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	let d_xx = List.nth vector 3 in
	let d_xy = List.nth vector 4 in
	let d_xz = List.nth vector 5 in
	y*.d_xx +. x*.d_xy -. b*.d_xz

let d'_yx vector t = 
	let d_yx = List.nth vector 6 in
	let d_yy = List.nth vector 7 in
	a*.(d_yy -. d_yx)

let d'_yy vector t = 
	let x = List.nth vector 0 in
	let z = List.nth vector 2 in
	let d_yx = List.nth vector 6 in
	let d_yy = List.nth vector 7 in
	let d_yz = List.nth vector 8 in
	(r -. z)*.d_yx -. d_yy -. x*.d_yz

let d'_yz vector t = 
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	let d_yx = List.nth vector 6 in
	let d_yy = List.nth vector 7 in
	let d_yz = List.nth vector 8 in
	y*.d_yx +. x*.d_yy -. b*.d_yz

let d'_zx vector t = 
	let d_zx = List.nth vector 9 in
	let d_zy = List.nth vector 10 in
	a*.(d_zy -. d_zx)

let d'_zy vector t = 
	let x = List.nth vector 0 in
	let z = List.nth vector 2 in
	let d_zx = List.nth vector 9 in
	let d_zy = List.nth vector 10 in
	let d_zz = List.nth vector 11 in
	(r -. z)*.d_zx -. d_zy -. x*.d_zz

let d'_zz vector t = 
	let x = List.nth vector 0 in
	let y = List.nth vector 1 in
	let d_zx = List.nth vector 9 in
	let d_zy = List.nth vector 10 in
	let d_zz = List.nth vector 11 in
	y*.d_zx +. x*.d_zy -. b*.d_zz

(*-------------------------------------------------------------------------------------*)

let rec rk4_solver fs state t h n =
	if n = 0 then 
		let x = List.nth state 0 in
		let y = List.nth state 1 in
		let z = List.nth state 2 in
		let d_xx = List.nth state 3 in
		let d_xy = List.nth state 4 in
		let d_xz = List.nth state 5 in
		let d_yx = List.nth state 6 in
		let d_yy = List.nth state 7 in
		let d_yz = List.nth state 8 in
		let d_zx = List.nth state 9 in
		let d_zy = List.nth state 10 in
		let d_zz = List.nth state 11 in
		Printf.printf "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" x y z d_xx d_xy d_xz d_yx d_yy d_yz d_zx d_zy d_zz

	else
		let f = f_vector fs in 
		let k1 = h *** (f state t) in
		let k2 = h *** (f (state ++ (0.5 *** k1)) (t +. h/.2.0) ) in
		let k3 = h *** (f (state ++ (0.5 *** k2)) (t +. h/.2.0) ) in
		let k4 = h *** (f (state ++ k3) (t +. h) ) in
		let new_state = state ++ (1.0/.6.0) *** (k1 ++ (2.0 *** k2) ++ (2.0 *** k3) ++ k4) in
		rk4_solver fs new_state (t +. h) h (n - 1)




let main () =
	let t0 = 0.0 in 
	let n  = 100000 in
	let dt = 0.001 in
	let x = float_of_string Sys.argv.(1) in
	let y = float_of_string Sys.argv.(2) in
	let z = float_of_string Sys.argv.(3) in
	let d_xx = 1.0 in
	let d_xy = 0.0 in
	let d_xz = 0.0 in
	let d_yx = 0.0 in
	let d_yy = 1.0 in
	let d_yz = 0.0 in
	let d_zx = 0.0 in
	let d_zy = 0.0 in
	let d_zz = 1.0 in
	let state = [x; y; z; d_xx; d_xy; d_xz; d_yx; d_yy; d_yz; d_zx; d_zy; d_zz] in
	let fs = [f1_lorenz; f2_lorenz; f3_lorenz; d'_xx; d'_xy; d'_xz; d'_yx; d'_yy; d'_yz; d'_zx; d'_zy; d'_zz] in
	rk4_solver fs state t0 dt n

let () = main ()

