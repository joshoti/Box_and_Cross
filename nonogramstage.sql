CREATE TABLE level(id int primary key, information varchar(1000));
INSERT INTO level(id, information)
values(1, '{"tiles": 63, "shape": 10, "grid_check": {"a": [[2], false], "b": [[1, 3, 1], false], "c": [[7], false], "d": [[1, 7], false], "e": [[9], false], "f": [[8], false], 
			"g": [[9], false], "h": [[1, 7], false], "i": [[1, 3, 1], false], "j": [[1, 1], false], "1": [[3], false], "2": [[5], false], "3": [[3], false], 
            "4": [[8], false], "5": [[6], false], "6": [[10], false], "7": [[9], false], "8": [[9], false], "9": [[3, 2], false], "10": [[3, 2], false]}, 
            "grid": [[5,5,5,5,0,0,0,5,5,5], [0,0,5,0,0,0,0,0,5,0], [5,0,0,0,0,0,0,0,0,5], [0,0,0,0,0,0,0,0,0,5], [5,5,0,0,0,0,0,0,5,5], [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,5], [0,0,0,0,0,0,0,0,0,0], [5,5,0,0,0,0,0,0,0,0], [5,0,0,0,0,5,0,0,0,5]], "solutionGrid": [[0,0,0,0,1,1,1,0,0,0], [0,0,0,1,1,1,1,1,0,0], 
            [0,0,0,0,1,1,1,0,0,0], [0,1,1,1,1,1,1,1,1,0], [0,0,1,1,1,1,1,1,0,0], [1,1,1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1,1,0], [0,1,1,1,1,1,1,1,1,1], 
            [0,0,1,1,1,0,1,1,0,0], [0,1,1,1,0,0,0,1,1,0]]}'),
		(2, '{"tiles": 53, "shape": 10, "grid_check": {"a": [[1], false], "b": [[2,1], false], "c": [[2,4], false], "d": [[10], false], "e": [[10], false], "f": [[6], false], 
			"g": [[3,1,2], false], "h": [[3,1,2], false], "i": [[1,2], false], "j": [[1,1], false], "1": [[4,3], false], "2": [[5,2], false], "3": [[2,2], false], 
            "4": [[5], false], "5": [[4], false], "6": [[7], false], "7": [[4], false], "8": [[6], false], "9": [[7], false], "10": [[2], false]}, 
            "grid": [[5,0,0,0,0,5,5,0,0,0], [0,0,0,0,0,0,0,0,0,5], [5,0,0,0,0,5,0,0,0,5], [0,5,0,0,0,0,0,5,0,5], [5,5,0,0,0,0,0,0,5,5], [0,0,0,0,0,0,0,0,5,0],
            [0,5,0,0,0,0,0,0,5,0], [0,0,5,0,0,0,0,0,0,0], [5,5,0,0,0,0,0,0,0,0], [5,0,5,0,0,5,0,0,5,0]], "solutionGrid": [[0,1,1,1,1,0,0,1,1,1], [1,1,1,1,1,0,1,1,0,0], 
            [0,0,0,1,1,0,1,1,0,0], [0,0,1,1,1,1,1,0,0,0], [0,0,1,1,1,1,0,0,0,0], [0,1,1,1,1,1,1,1,0,0], [0,0,1,1,1,1,0,0,0,0], [0,0,0,1,1,1,1,1,1,0], 
            [0,0,0,1,1,1,1,1,1,1], [0,0,0,1,1,0,0,0,0,0]]}');
