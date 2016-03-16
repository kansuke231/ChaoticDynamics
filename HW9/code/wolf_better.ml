(* This code is for calculating Lyapunov exponent of a system using wolf's algorithm.*)

type point = { x:float; y:float; z:float}

let eps = 1.6
exception No_nearest_point_found

let log2 x =
	(log10 x)/.(log10 2.0)

let read file = Core.Std.In_channel.read_lines file

let dot v1 v2 = (v1.x *. v2.x) +. (v1.y *. v2.y) +. (v1.z *. v2.z)

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

let abs_vec v =
	sqrt((v.x)**2. +. (v.y)**2. +. (v.z)**2.)

let ( -- ) v1 v2 =
	(* generate a vector v1 - v2*)
	{x = v1.x -. v2.x ; y = v1.y -. v2.y; z = v1.z -. v2.z}


let rec theiler_windows arr p last acc = 
	if (p > last) || (p >= Array.length arr)
		then acc
	else
		let new_acc = acc @ [arr.(p)] in
		theiler_windows arr (p+1) last new_acc

let rec nearest_neighbor arr p not_these i tip_index =
	(* p is the current point 
	   i is an index for arr
	   tip_index is an index for a point which exceeded the limit epsilon
	 *)
	if (i >= Array.length arr) then arr.(i-1), i-1
	else
	(
		if (not (exists arr.(i) not_these)) then
		(
			(* let d_i = distance arr.(i) p in *)
			let normal_vec = arr.(tip_index) -- p in 
			let target_vec = arr.(i) -- p in  
			let dot_result = dot normal_vec target_vec in 
			let theta = acos (dot_result/.((abs_vec normal_vec) *. (abs_vec target_vec))) in
			(* Printf.printf "dot_result:  %f\n" dot_result;
			Printf.printf "theta:  %f\n" theta; *)
			(* let d_min = distance min p in  *)
			if (eps > dot_result) && (theta < 1.74) then 
				arr.(i), i
			else
				nearest_neighbor arr p not_these (i+1) tip_index
		)
		else
			nearest_neighbor arr p not_these (i+1) tip_index
	)

let rec track_diff_traj arr i j d = 
	if (i >= Array.length arr) || (j >= Array.length arr) then 
		i,j,d
	else
	(
		let x = arr.(i) in
		let y = arr.(j) in 
		let new_d = distance x y in
		if new_d > eps then 
			i+1, j, new_d
		else
			track_diff_traj arr (i + 1) (j + 1) new_d
	)


let rec wolf arr i acc tip_index = 
	if (i >= Array.length arr) then 
		acc
	else
		let x_i = arr.(i) in 
		let dont_take_these = theiler_windows arr (i - 50) (i + 50) [] in
		let z_i, j = nearest_neighbor arr x_i (dont_take_these @[x_i]) 0 tip_index in
		let first_L = distance x_i z_i in 
		Printf.printf "i:%d j:%d\n" i j;
		let new_i, new_tip, last_L = track_diff_traj arr i j first_L in 
		Printf.printf "new_i:%d\n" new_i;
		wolf arr new_i (acc +. (log2 (last_L/.first_L))) new_tip


let main () =
	let point_array = Sys.argv.(1) |> read |> to_pointList |> Array.of_list in
	let result = wolf point_array 500 0.0 0 in
	Printf.printf "%f\n" (result/.20.)

let () = main ()

