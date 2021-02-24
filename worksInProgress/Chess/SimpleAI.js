//-----------------Build Board-------------------//

config = {
    position: 'start',
    draggable: true,
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
}
const board1 = ChessBoard("board1", config);
const bElem = document.getElementById("board1")

//-----------------------------------------------//


//------------------Build Game-------------------//
  //---------Algebra and Chess Notation--------//

  const chess = new Chess()

//-----------------------------------------------//

//------------Plays Random Legal Moves-----------//

function playRandomMove(){
    if(chess.game_over()) return//No play if gameover

    let moves = chess.moves() //List of all legal moves
    let move = moves[Math.floor(Math.random()*moves.length)] //a randomly selected legal move
    
    return move
    
    /*
    chess.move(move) //make it

    board1.position(chess.fen()) //update board to match
    */
}

//-----------------------------------------------//

//-----Will Capture Via ~Some Method if Able-----//

function playForCapture(){
    if(chess.game_over()) return //No play if gameover

    let possibleCapture = false;
    let moves = chess.moves({verbose: true})
    let move

    for(i = 0; i < moves.length; ++i){//Iterates every move looking for a capture
        let curMove = moves[i]
        if(curMove.flags == 'c' || curMove.flags == 'e'){
            possibleCapture = true
            move = curMove
        }
    }

    if(possibleCapture){
        chess.move(move)
        board1.position(chess.fen())
    }else{
        playRandomMove()
    }
   
}

//-----------------------------------------------//

//--------------Position Evaluation-------------//

/*
current best evaluation = current evaluation

For each move
    make move
    evaluate board
    if evaluation score is better than current best
        store move index
    undo move

make best move **STILL TECHNICALLY SINGLE MOVE CAPTURE**
*/
function findBestNext(){
    if(chess.game_over()) return //No play if gameover
    
    let currEval = evaluateBoard(chess)
    console.log("Current Numeric Evaluation: " + currEval)
    
    let moves = chess.moves()
    console.log("Possible moves: " + moves)
    
    let moveFound = false
    let move

    console.log("Number of possible moves: " + moves.length)

    for(let i = 0; i < moves.length; i++){
        chess.move(moves[i])
        testEval = evaluateBoard()
        if(testEval > currEval){
            currEval = testEval
            move = moves[i]
            moveFound = true
        }
        chess.undo()
    }

    if(moveFound){
        console.log("Move found: " + move)
        chess.move(move)
        board1.position(chess.fen())
    }else{
        console.log("No best move found.")
        playRandomMove()
    }
}

/*
    take in current chess object
    for each pieceChar of fen
        add pieceChar value to evalTotal
    return evalTotal
*/
function evaluateBoard(board = chess){
    
    let eFen = board.fen()
    let pieces = eFen.split(" ")[0]
    let evaluation = 0
    for(let i = 0; i < pieces.length; i++){
        let j = pieces.charAt(i)
        if(isNaN(j) && j !== '/'){
            evaluation += valueTable[j]
        }
    }
    return evaluation
}


/*
Consider move paths, travel down each move path to a distance DEPTH
Evaluate leaves/nodes at DEPTH level
Move path with strongest leaf evaluation is followed
*/
function minimaxRoot(depth, isMaximisingPlayer) {

    let moves = chess.moves();
    let bestMove = -9999;
    let bestMoveFound;

    for(let i = 0; i < moves.length; i++) {
        let move = moves[i];
        chess.move(move);
        let value = minimax(depth - 1, !isMaximisingPlayer);
        chess.undo();
        if(value >= bestMove) {
            bestMove = value;
            bestMoveFound = move;
        }
    }
    return bestMoveFound;
};

function minimax (depth, isMaximisingPlayer) {
    //positionCount++;
    if (depth === 0) {
        return -evaluateBoard();
    }

    let moves = chess.moves();

    if (isMaximisingPlayer) {
        let bestMove = -9999;
        for (let i = 0; i < moves.length; i++) {
            chess.move(moves[i]);
            bestMove = Math.max(bestMove, minimax(depth - 1, !isMaximisingPlayer));
            chess.undo();
        }
        return bestMove;
    } else {
        let bestMove = 9999;
        for (let i = 0; i < moves.length; i++) {
            chess.move(moves[i]);
            bestMove = Math.min(bestMove, minimax(depth - 1, !isMaximisingPlayer));
            chess.undo();
        }
        return bestMove;
    }
};

//-----------------------------------------------//


//--------------Playability Functions------------//

function playBestMove(){
    let move = minimaxRoot(DEPTH, true)
    console.log("Best move at depth 3: " + move)
    chess.move(move)
}

function onDragStart(source, piece, position, orientation){

    if(chess.game_over()) return false //No moving if gameover

    if(piece.search(/^b/) !== -1) return false //No moving black's pieces
}

function onDrop(source, target){  //Place your piece
    let move = chess.move({from: source, to: target, promotion: 'q'}) //promote to queen for ease
    if(move === null) return 'snapback'  //Illegal moves get snapped back

    window.setTimeout(playBestMove(),0)
    

}

//For en passant, castling and promotions
function onSnapEnd(){
    board1.position(chess.fen())
}

//-----------------------------------------------//

//---------------Constants, lets, etc.-----------//
const valueTable = {
    'p': 10, 'P': -10,
    'n': 30, 'N': -30,
    'b': 30, 'B': -30,
    'r': 50, 'R': -50,
    'q': 90, 'Q': -90,
    'k': 999, 'K': -999
}   
let positionsCount = 0
let playerValue = 390+999
const DEPTH = 3
//-----------------------------------------------//
