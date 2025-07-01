# NQL Overview and Syntax

The Netography Query Language (NQL) is the basis for accomplishing many tasks in Fusion.

- Searching for flows, DNS, events, audits, or block records
- Filtering statistics and aggregations
- Defining custom Detection Models to create an event 

# Using NQL in Fusion

NQL can be used in Detection Models, or to define widgets inside custom dashboards. It can be used in the API as the value for the `search` parameter if it exists.

# NQL Syntax

## NQL Examples

| Description           | NQL                                                                |
| --------------------- | ------------------------------------------------------------------ |
| IP Reputation Matches | `srciprep.count > 0 OR dstiprep.count > 0`                         |
| Only Privileged Ports | `dstport < 1024`                                                   |
| Not Broadcast IPs     | `dstip != 255.255.255.0/24`                                        |
| TCP Ports Scan        | `tcpflags.syn == true and tcpflags.ack == true and srcport > 1024` |

## NQL Basics

Using the Netography Query Language is like writing a programming conditional inside an `if ( )` statement. The statement should be constructed logically, from left to right, comparing fields to values.

## Rules and Limitations

### Spacing and Parentheses

- Operators must be surrounded by spaces, e.g. `srcip == 10.0.0.1` is valid, while `srcip==10.0.0.1` is not valid.
- Whitespace is **not optional** in NQL. For example, `input==1` is invalid, but `input == 1` is valid since the NQL parser will not parse the first example if the whitespace is missing.
- NQL accepts nested parentheses. For example, `((this) || (that)) && other` is a valid NQL statement. However, this can be considered hard to read, so it is suggested to reduce the use of parentheses when possible, e.g. `(this || that) && other`
- Logic must be unambiguous. e.g. `A && B || C` will fail. Use parentheses `()` to prevent ambiguity

### Comparisons

- Only integer fields can use numerical comparisons: `< <= > >=`

### CIDR Notation

- IP fields can be searched with CIDR notation if desired. For example, `10.0.0.0/24` will match `10.0.0.1`

## Operators

> ❓ What is an operator?
> 
> In the context of NQL, operators are used to define how fields should be compared or matched against values, allowing users to filter, search, and analyze data according to specific criteria.

## Boolean Operators

| Boolean    | Description                                   | Example                |
| :--------- | :-------------------------------------------- | :--------------------- |
| `&&` `AND` | logical AND                                   | `this && that`         |
| `OR`       | logical OR                                    | `this OR that`         |
| `!`        | NOT _must precede expressions in parenthesis_ | `!(srcip == 10.0.0.1)` |

## Comparison Operators

| Comparison | Description               |
| ---------- | ------------------------- |
| `==`       | equals                    |
| `!=`       | not equals                |
| `<=`       | less than or equals to    |
| `<=`       | less than                 |
| `>=`       | greater than or equals to |
| `>`        | greater tha               |

# Pattern Matching (Wildcards, RegEx, Fuzzy) in NQL

In NQL, pattern matching is performed using regular expressions, wildcards, and fuzzy matching. The operators `=~` and `!~` specify these matches and their negative counterparts.

> ℹ️ NQL fields supporting pattern matching
> 
> Pattern matching is only supported for the fields listed below.
> 
> | Category | Fields                                                                |
> | :------- | :-------------------------------------------------------------------- |
> | Flow     | `dstiprep.categories srciprep.categories tags`                        |
> | DNS      | `answers.rdata query.domain query.host query.name query.publicsuffix` |
> | Events   | `ipinfo.iprep.categories summary tags`                                |
> | Audit    | `description`                                                         |

## Wildcards

Wildcards use special characters to match patterns of text.

### Wildcards: Operator Syntax and Meaning

| Operator | Syntax | Meaning                                              | Example Field       |
| -------- | ------ | ---------------------------------------------------- | ------------------- |
| `=~`     | `*at`  | Matches zero or more characters.                     | `query.name =~ *at` |
| `!~`     | `*at`  | Negative match for zero or more characters.          | `query.name !~ *at` |
| `=~`     | `?at`  | Matches any single character before "at".            | `query.name =~ ?at` |
| `!~`     | `?at`  | Negative match for any single character before "at". | `query.name !~ ?at` |

**Note**: Avoid beginning patterns with `*` or `?` as this can lead to performance issues due to increased iterations.

## Regular Expressions (regex)

Regular expressions (regex) allow for flexible and complex search patterns. In NQL, you can use regex to match patterns with precise rules.

**Note**: Avoid beginning patterns with `*` or `?` as this can lead to performance issues due to increased iterations.

### Regex: Examples

```Text NQL
query.domain =~ net_  
query.domain =~ netog.i?  
query.domain =~ net~  
query.domain =~ /[a-z]_/  
query.domain =~ /[a-z]\_/ && query.name == neto
```

### Regex: Operator Syntax and Meaning

| Operator | Syntax   | Meaning                                     | Example Field                |
| -------- | -------- | ------------------------------------------- | ---------------------------- |
| `=~`     | `/.*at/` | Matches zero or more characters.            | `query.name =~ /net.*\.com/` |
| `!~`     | `/.*at/` | Negative match for zero or more characters. | `query.name !~ /net.*\.com/` |

### Regex: Text Boundary Anchors

Boundary anchors specify positions in the text. The start and end characters are implicitly applied to each search and cannot be modified:

| Regexp | Meaning                   | Description                   | Example                  |
| ------ | ------------------------- | ----------------------------- | :----------------------- |
| `^`    | Start of a line or string | Matches the start of a string | `^cat` matches  `catdog` |
| `$`    | End of a line or string   | Matches the end of a string   | `cat$` matches `dogcat`  |

### Regex: Choice and Grouping

Choice and grouping operators allow you to match one or more alternatives or group expressions:

| Regexp      | Meaning         | Description               | Example                                               |
| :---------- | :-------------- | :------------------------ | :---------------------------------------------------- |
| `xy`        | x followed by y | Matches "xy"              | `abc\` matches "abc".                                 |
| `x OR y`    | x or y          | Matches "x" or "y"        | ye\` matches "axe" or "aye"                           |
| `abc(def)?` | Grouping        | Matches "abc" or "abcdef" | `abc(def)?` matches `abc` and `abcdef` but not `abcd` |

### Regex: Repetition (Greedy and Non-Greedy)

Repetition operators match a specified number of occurrences:

| Regexp   | Meaning                          | Description                                                                    |
| -------- | -------------------------------- | ------------------------------------------------------------------------------ |
| `x*`     | Zero or more occurrences of x    | Matches zero or more of "x". Example: `a*` matches "", "a", "aa".              |
| `x+`     | One or more occurrences of x     | Matches one or more of "x". Example: `a+` matches "a", "aa".                   |
| `x?`     | Zero or one occurrence of x      | Matches zero or one of "x". Example: `a?` matches "" or "a".                   |
| `x{n,m}` | Between n and m occurrences of x | Matches between n and m of "x". Example: `a{2,4}` matches "aa", "aaa", "aaaa". |
| `x{n,}`  | n or more occurrences of x       | Matches n or more of "x". Example: `a{2,}` matches "aa", "aaa".                |
| `x{n}`   | Exactly n occurrences of x       | Matches exactly n of "x". Example: `a{3}` matches "aaa".                       |

### Regex: Character Classes

Character classes match specific sets or ranges of characters:

| Regexp   | Meaning                                     | Description                                                                               |
| -------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `.`      | Matches any single character                | Matches any character except a newline. Example: `c.t` matches "cat" and "cot".           |
| `[abc]`  | Matches any single character in the set     | Matches one of "a", "b", or "c". Example: `[aeiou]` matches any vowel.                    |
| `[^abc]` | Matches any single character not in the set | Matches any character except "a", "b", or "c". Example: `[^aeiou]` matches consonants.    |
| `[a-z]`  | Matches any single character in the range   | Matches any character between "a" and "z". Example: `[a-z]` matches any lowercase letter. |

### Regex: Numeric Ranges

Numeric ranges match numbers within a specific range, providing greater flexibility for queries involving numeric values.

| Regexp     | Meaning                                     | Description                                                              |
| ---------- | ------------------------------------------- | ------------------------------------------------------------------------ |
| `<1-10>`   | Any number between 1 and 10                 | Matches any numeric value between the 2 numbers                          |
| `<01-010>` | Any number between 1 and 10 with leading 0s | Matches any numeric value between the 2 numbers, including leading zeros |

#### Numeric range examples

`query.name =~ /ip-(<0-255>-?){3}(<100-200>)\..*/`  
Matches ip-\<0-255>.\<100-200>.x.x.

`query.name =~ foo<1-100>`  
Matches "foo1", "foo2", ..., "foo100".

#### Numeric range performance

Using numeric range matching can simplify queries for numerical intervals but may increase execution time if used with large ranges or complex regex patterns. As with other regex patterns, avoid starting expressions with `*` or `?` when combining them with numeric ranges to prevent performance degradation.

### Regex: Special Characters

Special characters perform specific functions within regex patterns:

| Regexp | Meaning          | Description                                                                                   |
| ------ | ---------------- | --------------------------------------------------------------------------------------------- |
| `\`    | Escape character | Escapes special characters to be treated as literals. Example: `\.` matches a literal period. |

#### Regex: Reserved Characters

The following characters are reserved as operators and need to be escaped: `. ? + * | { } [ ] ( ) " \`

## Fuzzy Matching

Fuzzy matching accounts for variations in spelling by calculating the Levenshtein distance between terms.

### Fuzzy Matching: Operator Syntax and Meaning

| Operator | Syntax  | Meaning                                                  | Example Field         |
| -------- | ------- | -------------------------------------------------------- | --------------------- |
| `=~`     | `cat~`  | Matches terms with an automatically calculated distance. | `query.name =~ cat~`  |
| `!~`     | `cat~`  | Negative fuzzy match with automatic distance.            | `query.name !~ cat~`  |
| `=~`     | `cat~2` | Matches terms with a maximum distance of 2 changes.      | `query.name =~ cat~2` |
| `!~`     | `cat~2` | Negative match with a maximum distance of 2 changes.     | `query.name !~ cat~2` |