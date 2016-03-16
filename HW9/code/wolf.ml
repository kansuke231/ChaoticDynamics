(* This code is for calculating Lyapunov exponent of a system using wolf's algorithm.*)

type point = { x:float; y:float; z:float}

let log2 x =
	(log10 x)/.(log10 2.0)

let read file = Core.Std.In_channel.read_lines file

let dot = List.fold_left2 (fun z x y -> z +. x *. y) 0.

let to_pointList lines =
	Core.Std.List.map lines
		~f:(fun s -> 
				Core.Std.String.split_on_chars s ~on:[','] 
			|> fun char_list ->
				let x = float_of_string(Core.Std.List.nth_exn char_list 1) in
				let y = float_of_string(Core.Std.List.nth_exn char_list 2) in
				let z = float_of_string(Core.Std.List.nth_exn char_list 3) in
				{x; y; z})

let exists k l =
    List.fold_left (fun b x -> b || x = k) false l

let distance a b =
	sqrt((a.x -. b.x)**2. +. (a.y -. b.y)**2. +. (a.z -. b.z)**2.)


let rec theiler_windows arr p last acc = 
	if (p > last) || (p >= Array.length arr)
		then acc
	else
		let new_acc = acc @ [arr.(p)] in
		theiler_windows arr (p+1) last new_acc

let rec nearest_neighbor arr p not_these i min min_p =
	(* p is the current point 
	   i is an index for arr
	   min is the point whose distance is minimum to p
	   min_p is an index for min point
	 *)
	if (i >= Array.length arr) then min,min_p
	else
	(
		if (not (exists arr.(i) not_these)) then
		(
			let d_i = distance arr.(i) p in
			let d_min = distance min p in 
			if d_min > d_i then 
				nearest_neighbor arr p not_these (i+1) arr.(i) i
			else
				nearest_neighbor arr p not_these (i+1) min min_p
		)
		else
			nearest_neighbor arr p not_these (i+1) min min_p
	)

let rec track_diff_traj arr eps i j d = 
	if (i >= Array.length arr) || (j >= Array.length arr) then 
		i,d
	else
	(
		let x = arr.(i) in
		let y = arr.(j) in 
		let new_d = distance x y in
		if new_d > eps then 
			i + 1,new_d
		else
			track_diff_traj arr eps (i + 1) (j + 1) new_d
	)


let rec wolf arr eps i acc = 
	if (i >= Array.length arr) then 
		acc
	else
		let x_i = arr.(i) in 
		let dont_take_these = theiler_windows arr (i - 50) (i + 50) [] in
		let z_i, j = nearest_neighbor arr x_i (dont_take_these @[x_i]) 0 arr.(0) 0 in
		let first_L = distance x_i z_i in 
		Printf.printf "i:%d j:%d\n" i j;
		let new_i, last_L = track_diff_traj arr eps i j first_L in 
		Printf.printf "new_i:%d\n" new_i;
		wolf arr eps new_i (acc +. (log2 (last_L/.first_L)))


let main () =
	let point_array = Sys.argv.(1) |> read |> to_pointList |> Array.of_list in
	let result = wolf point_array 1.6 500 0.0 in
	Printf.printf "%f\n" (result/.20.)

let () = main ()

