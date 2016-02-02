function fractal_tree(origin,dest,theta,ratio,depth)

    % when reaching to a leaf
    if depth == 0
        %disp('End');
        return
    end
    
    x1 = origin(1); x2 = dest(1);
    y1 = origin(2); y2 = dest(2);
    % draw a line
    line([x1,x2],[y1,y2]);
    
    vector = [x2-x1 y2-y1];
    new_origin = dest;
    
    for e = [theta, -theta]
        rotation = ratio*[cos(e) -sin(e); sin(e) cos(e)]
        new_vector = vector*rotation
        new_dest = new_origin + new_vector
        fractal_tree(new_origin, new_dest, theta, ratio, depth -1);
    end
    
    