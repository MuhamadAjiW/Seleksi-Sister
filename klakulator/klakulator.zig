//di zig gaada goto co wtf tanggung jawab

fn leftmostloc(a: i32) i32 {
    const edge: u32 = 1 << 31;
    var roam: u32 = @bitCast(u32, a);

    var counter: i32 = 0;
    while (roam & edge == 0) {
        roam = roam << 1;
        counter = counter + 1;
    }
    return counter;
}

fn add(a: i32, b: i32) i32 {
    var carry: i32 = 0;
    var noncarry: i32 = 0;
    var temp: i32 = 0;

    carry = a & b;
    noncarry = a ^ b;

    while (carry != 0) {
        carry = carry << 1;
        temp = noncarry;
        noncarry = noncarry ^ carry;
        carry = temp & carry;
    }
    return noncarry;
}

fn subtr(a: i32, b: i32) i32 {
    return add(add(a, ~b), 1);
}

fn mult(a: i32, b: i32) i32 {
    var x: i32 = a;
    var y: i32 = b;
    var result: i32 = 0;
    var negative: bool = false;

    if (x < 0) {
        x = ~x;
        x = add(x, 1);
        negative = !negative;
    }
    if (y < 0) {
        y = ~y;
        y = add(y, 1);
        negative = !negative;
    }

    while (y != 0) {
        if (y & 1 == 1) result += x;
        x = x << 1;
        y = y >> 1;
    }

    if (negative) {
        return add(~result, 1);
    } else {
        return result;
    }
}

fn div(a: i32, b: i32) i32 {
    var x: i32 = a;
    var y: i32 = b;
    var result: i32 = 0;
    var negative: bool = false;
    var limit: i32 = leftmostloc(b);

    if (x < 0) {
        x = ~x;
        x = add(x, 1);
        negative = !negative;
    }
    if (y < 0) {
        y = ~y;
        y = add(y, 1);
        negative = !negative;
    }

    // if (y << 31 <= x) {
    //     x = subtr(x, y << 31);
    //     result = add(result, 1 << 31);
    // }

    var i: u5 = 31;
    var one: i32 = 1;
    while (i != 0) {
        if ((y << i) <= x and limit > i) {
            x = subtr(x, y << i);
            result = add(result, one << i);
        }
        i = i - 1;
    }
    if (y <= x and limit > 0) {
        x = subtr(x, y);
        result = add(result, 1);
    }

    if (negative) {
        return add(~result, 1);
    } else {
        return result;
    }
}

fn exp(a: i32, b: i32) i32 {
    var x: i32 = a;
    var y: i32 = b;

    var result: i32 = 1;
    var bitone: i32 = 1;

    while (y != 0) {
        bitone = y & 1;
        if (bitone == 1) result = mult(result, x);
        x = mult(x, x);
        y = y >> 1;
    }
    return result;
}

// mesin kata dulu gak sih
fn stream_procnum(string: []const u8, pointer: *i32) i32 {
    var result: i32 = 0;
    var negative: bool = false;

    if (string[0] == '-') {
        negative = true;
        pointer.* = add(pointer.*, 1);
    }

    while (string[@intCast(usize, pointer.*)] >= '0' and string[@intCast(usize, pointer.*)] < '9') {
        result = add(mult(result, 10), (string[@intCast(usize, pointer.*)] - '0'));
        pointer.* = add(pointer.*, 1);
    }
    if (negative) {
        return mult(-1, result);
    } else {
        return result;
    }
}

fn stream_skipws(string: []const u8, pointer: *i32) void {
    while (string[@intCast(usize, pointer.*)] == ' ') {
        pointer.* = add(pointer.*, 1);
    }
}

const print = std.debug.print;
const std = @import("std");
pub fn main() !void {
    const stdin = std.io.getStdIn().reader();

    print("Enter a math expression: ", .{});
    var expression: [64]u8 = undefined;
    var pointer: i32 = 0;
    var input = try stdin.readUntilDelimiterOrEof(&expression, '\n');
    _ = input;

    var operand1: i32 = 0;
    var operand2: i32 = 0;
    var operator: u8 = 0;
    var valid: bool = true;

    stream_skipws(&expression, &pointer);
    operand1 = stream_procnum(&expression, &pointer);
    while (expression[@intCast(usize, pointer)] != '\n' and expression[@intCast(usize, pointer)] != '\r' and valid) {
        stream_skipws(&expression, &pointer);

        if (expression[@intCast(usize, pointer)] == '\n' and expression[@intCast(usize, pointer)] == '\r') {
            break;
        }

        operator = expression[@intCast(usize, pointer)];
        pointer = add(pointer, 1);
        stream_skipws(&expression, &pointer);

        operand2 = stream_procnum(&expression, &pointer);

        switch (operator) {
            '+' => {
                operand1 = add(operand1, operand2);
            },
            '-' => {
                operand1 = subtr(operand1, operand2);
            },
            '*' => {
                operand1 = mult(operand1, operand2);
            },
            '/' => {
                operand1 = div(operand1, operand2);
            },
            '^' => {
                operand1 = exp(operand1, operand2);
            },
            else => {
                print("Invalid operator\n", .{});
                valid = false;
            },
        }
    }
    print("Result: {d}\n", .{operand1});
}
